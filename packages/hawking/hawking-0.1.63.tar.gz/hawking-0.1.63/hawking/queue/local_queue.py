
import os
import json
import logging
import sqlite3
import threading

class LocalQueue():
    def __init__(self, queue_path):
        self.db_file = os.path.join(queue_path, "queue.db")
        logging.info("Use {} file".format(self.db_file))

        connection = sqlite3.connect(self.db_file)
        try:
            connection.execute("CREATE TABLE IF NOT EXISTS queue (checkpoint INTEGER PRIMARY KEY, namespace VARCHAR(1024), document JSON NOT NULL);")
            connection.commit()
        finally:
            connection.close()

        self.condition = threading.Condition()


    def _poll(self, checkpoint):
        connection = sqlite3.connect(self.db_file)
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT namespace, document FROM queue WHERE checkpoint = ?", (checkpoint,) )

            row = cursor.fetchone()
            if row is None:
                return None

            return {"namespace": row[0], "document": row[1] }
        finally:
            connection.close()

    def Poll(self, request, context=None):
        """
            option (google.api.http) = {
                post: "/v1/post"
                body: "*"
            };
        """
        checkpoint = 1 if request['checkpoint'] is None or request['checkpoint'] == '' else int(request['checkpoint'])
        logging.info("{} start with checkpoint {}".format("local" if context is None else context.peer(), checkpoint))

        while True:
            response = None
            self.condition.acquire()

            item = self._poll(checkpoint)
            while item is None:
                self.condition.wait()
                item = self._poll(checkpoint)
            self.condition.release()

            checkpoint += 1
            namespace = item['namespace']
            record = json.loads(item['document'])
            response = {"checkpoint": str(checkpoint),
                "namespace": namespace,
                "document": {"uuid": record['uuid'], "body": record['content']}
            }

            yield response


    def Post(self, request, context=None):
        """
            option (google.api.http) = {
                post: "/v1/post"
                body: "*"
            };
        """
        self.condition.acquire()

        connection = sqlite3.connect(self.db_file)
        try:
            for document in request['documents']:
                logging.info('Enqueue "{}/{}/{}"'.format(request['namespace'], document['uuid'], document['body']))
                connection.execute("INSERT INTO queue (namespace, document) VALUES (?, ?)",
                    (request['namespace'], json.dumps({"uuid":document['uuid'], "content": document['body']}))
                )
                
            connection.commit()
        finally:
            connection.close()

        self.condition.notifyAll()
        self.condition.release()
