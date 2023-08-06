""" Faiss Index Server.

"""
import json
import os
import logging
import time

import click
import grpc

from concurrent import futures
from hawking_proto import hawking_pb2, hawking_pb2_grpc
from hawking.serve import configure_logging
from hawking.common import info


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class TsvIndexIterator:
    def __init__(self, source_file):
        info('Creating TsvIterator.')
        self.source_file = source_file
        self._handle = open(self.source_file, 'r')
        self.schema = None

    def next(self):
        line = 0
        for row in self._handle:
            try:
                if len(row) == 0:
                    continue
                if row.startswith('#schema:'):
                    self.schema = row[len('#schema:'):].split(',')
                    continue
                if self.schema is None and line > 1:
                    logging.error('Schema cannot be determined. Expecting #schema:field1,...,field2 signature.')
                    break
                if self.schema is not None and row.startswith('#'):
                    continue
                record = {}
                row = row.strip()
                tokens = row.split('\t')
                if len(tokens) != len(self.schema):
                    logging.error('Record {}:`{}...`, does not conform to the schema. Expected: {}. Actual: {}'.format(
                        line + 1, row[:25], len(self.schema), len(tokens)))
                    continue
                for i in range(0, len(self.schema)):
                    record[self.schema[i]] = tokens[i]
            finally:
                line = line + 1
            yield record
        self._handle.close()


class CaptionServicer(hawking_pb2_grpc.CaptionServicer):
    """ Implements hawking_pb2_grpc.CaptionServicer. """

    def __init__(self, index_path):
        self.LoadIndex(index_path)

    def LoadIndex(self, index_path):
        """ Load forward index. """
        assert os.path.exists(index_path), "Index {} does not exist!".format(index_path)
        logging.info('Loading index {}'.format(index_path))
        st = time.time()
        self.forward_index = []
        self.iterator = TsvIndexIterator(index_path)
        for record in self.iterator.next():
            self.forward_index.append(record)
        self.total_docs = len(self.forward_index)
        et = time.time() - st
        logging.info('Index loaded. Elapsed time: %.2f s' % et)

    def Get(self, request, context):
        logging.info('Receive query: {}'.format(request))

        response = hawking_pb2.SnippetResponse()
        for doc_id in request.doc_ids:
            if doc_id < self.total_docs:
                record = self.forward_index[doc_id]
                print(record)
                (title, body, metadata) = self._get_snippet(record)
            # We may not have title, body, and the application can look at metadata field.
            response.snippets.append(hawking_pb2.Snippet(title=title, body=body, metadata=metadata))
        logging.info('Response:{}'.format(response))
        return response

    def _get_snippet(self, record):
        """ Simple get snippet heuristics.

        Heuristics:
            - Find any field with 'title' or 'description', classify the rest into metadata.
            - If there is only 1 field, set this field as title
            - If there is only 2 fields, set this field as (title, body)
            - If there is only 3 fields, set first, second, third as (title, body, metadata)
        """
        kv = [v for (i, v) in enumerate(record.items()) if i == 0]
        if len(record.items()) == 1:
            return kv[0][1], None, None
        elif len(record.items()) == 2:
            return kv[0][1], kv[1][1], None
        elif len(record.items()) == 3:
            return kv[0][1], kv[1][1], kv[2][1]

        title = ''
        body = ''
        metadata = {}

        for key, value in record.items():
            if key == 'title':
                title = value
            elif key == 'body' or key == 'description':
                body = value
            else:
                metadata[key] = value
        return title, body, json.dumps(metadata)


def serve(index_path, worker_threads, grpc_port):
    configure_logging()

    logging.info('TAG: CAPTION')
    logging.info('Starting gRPC index server ...')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=worker_threads))
    caption_servicer = CaptionServicer(index_path)
    hawking_pb2_grpc.add_CaptionServicer_to_server(caption_servicer, server)
    server.add_insecure_port('[::]:{}'.format(grpc_port))
    server.start()
    logging.info('Ready to serve. Listening on 0.0.0.0:{}'.format(grpc_port))
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


@click.command()
@click.option('--index-path', help="Index path.", default=None)
@click.option('--worker-threads', '-w', help="Maximum numbers of worker threads.", default=10)
@click.option('--grpc-port', help="gRPC port to listen to request.", default=50001)
def run(index_path, worker_threads, grpc_port):
    serve(index_path, int(worker_threads), int(grpc_port))


if __name__ == "__main__":
    run()
