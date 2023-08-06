import logging
import time
import grpc
import threading
import json
import numpy
import sys

from hawking.queue.local_queue import LocalQueue
from hawking.encoder.universal.encoder import UniversalTextEncoder

def _cos_similarity(f1, f2):
    n1 = numpy.linalg.norm(f1)
    n2 = numpy.linalg.norm(f2)

    return numpy.dot(f1, f2) / (n1 * n2)

# Default search engine
class LocalSearchEngine():
    def __init__(self, queue_path):
        self.queue = LocalQueue(queue_path)
        self.encoder = UniversalTextEncoder()
        self.namespaces = {}
        self.checkpoint = None
        self.lock = threading.Lock()

        logging.info("Start new LocalIndex")
        threading.Thread(daemon=True, name="poll-thread", target=self._poll).start()

    def _poll(self):
        for index in self.queue.Poll(request={'checkpoint': self.checkpoint}):
            namespace = index['namespace']
            uuid = index['document']['uuid']
            logging.info('Checkpoint {} "{}/{}/{}" to index'.format(index['checkpoint'], 
                namespace, uuid, index['document']['body']))
            features = self.encoder.batch_encode([index['document']['body']])[0]
            self.checkpoint = index['checkpoint']

            with self.lock:
                if namespace not in self.namespaces:
                    self.namespaces[namespace] = {}
                self.namespaces[namespace][uuid] = features
 
    # request to index single entity
    # reference - unique way to refer
    # documents - all embeddings of entity
    #
    # returns: true, if new entry was added, false if existing entry was updated
    def index(self, namespace, uuid, body):
        logging.info('Add "{}/{}/{}"'.format(namespace, uuid, body))

        self.queue.Post(request={
            "namespace": namespace, 
            "documents": [{'uuid': uuid, 'body': body}],
        })
            

    # search through entities (match query with embeddings of entity)
    # count - max number of results
    # query - search query
    #
    # returns: array of tuples (reference -> score)
    def search(self, namespace, count, query):
        results = []

        features = self.encoder.batch_encode([query])[0]

        with self.lock:
            if namespace not in self.namespaces:
                logging.info('Namespace "{}" not indexed'.format(namespace))
                return results

            # Match query terms with embedings 
            for k,v in self.namespaces[namespace].items():
                # score is distance between 
                score = _cos_similarity(v, features)
                results.append((k, score))

        logging.info('{} results found'.format(len(results)))

        # sort results, in asc of score
        results.sort(key=lambda result: result[1], reverse=True)

        # return top #count# results
        return results[:count]        