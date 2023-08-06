""" A module for building Faiss index.
"""
import numpy as np
import time

from faiss import IndexHNSWFlat, read_index, write_index


def log(skk):
    print("\033[92m {}\033[00m".format(skk))


def _build_index(embedding_file, dimension, batch_size=50000, HNSW_M=32):
    """ Build Faiss index from embedding_file in batch_size at a time.

    embedding_file: <metadata>\t<v0|v1|...|vk>\n
    batch_size: number of batch to add to index at a time
    dimension: embedding dimension
    output: index output path
    HNSW_M: the maximum number of outgoing connections in the graph
    """
    log('Loading index ...')
    index = IndexHNSWFlat(dimension, HNSW_M)
    st = time.time()
    with open(embedding_file, 'r') as f:
        rows = []
        for record in f:
            record = record.strip()
            tokens = record.split('\t')
            # TODO(oleg): store metadata into table
            metadata = tokens[0]
            value = tokens[1].split('|')
            rows.append(value)
            if len(rows) >= batch_size:
                _st = time.time()
                index.add(np.array(rows).astype('float32'))
                _et = time.time() - _st
                print('indexing %d rows. Elapsed time: %.2f s. Rate: %.2f dps' % (len(rows), _et, len(rows) / _et))
                rows = []
        _st = time.time()
        index.add(np.array(rows).astype('float32'))
        _et = time.time() - _st
        print('indexing %d rows. Elapsed time: %.2f s. Rate: %.2f dps' % (len(rows), _et, len(rows) / _et))
        rows = []

    log('Building index completed.')
    log('Statistics:')
    log('Doc #count: {}'.format(index.ntotal))
    log('Elapsed time: %.2f s' % (time.time() - st))
    return index


def build_index(embedding_file, batch_size, dimension, output, HNSW_M=32):
    """ Build Faiss index.

    embedding_file: <metadata>\t<v0|v1|...|vk>\n
    batch_size: number of batch to add to index at a time
    dimension: embedding dimension
    output: index output path
    HNSW_M: the maximum number of outgoing connections in the graph
    """
    log('Building {} file ...'.format(output))
    log("  Input     : {}".format(embedding_file))
    log("  HNSW_M    : {}".format(HNSW_M))
    log("  Dimension : {}".format(dimension))
    log("  BatchSize : {}".format(batch_size))

    index = _build_index(embedding_file, dimension, batch_size, HNSW_M)

    def query_fn(index, n, dimension, k):
        print(n)
        for i in range(n):
            rand_query = np.random.random((1, dimension)).astype('float32')
            index.search(rand_query, k)

    def batch_query_fn(index, n, dimension, k):
        xq = np.random.random((n, dimension)).astype('float32')
        index.search(xq, k)

    def test_query(index, n, k=10, query_fn=query_fn):
        log('Executing {} queries ...'.format(n))

        st = time.time()
        query_fn(index, n, dimension, k)
        et = time.time() - st
        log('Completed executing %d queries. Elapsed time %.2f s. Rate: %.2f qps' % (n, et, n / et))

    test_query(index, 1000, k=10, query_fn=query_fn)
    test_query(index, 1000, k=10, query_fn=batch_query_fn)
    write_index(index, output)
