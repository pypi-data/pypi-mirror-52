import json
import os
import time

from random import random, shuffle

from hawking.index.faiss import build_index
from hawking.encoder import create_encoder
from hawking.common import info


class TextIterator:
    def __init__(self, source_file):
        info('Creating TextIterator.')
        self.source_file = source_file
        self._handle = open(self.source_file, 'r')

    def next(self):
        for line in self._handle:
            yield line.strip()
        self._handle.close()


class UrlIterator:
    def __init__(self, source_file):
        info('Creating UrlIterator.')
        self.source_file = source_file
        self._handle = open(self.source_file, 'r')

    def next(self):
        for line in self._handle:
            assert line.startswith('http')
            yield line.strip()
        self._handle.close()


class TsvIterator:
    def __init__(self, source_file, column_index=0):
        """ Instantiates TsvIterator
        :param source_file: filename
        :param column_idx: idx of the column to be retrieved
        """
        info('Creating TsvIterator.')
        self.column_index = column_index
        self.source_file = source_file
        self._handle = open(self.source_file, 'r')

    def next(self):
        for line in self._handle:
            if len(line) == 0:
                continue
            if line.startswith('#'):
                continue
            tokens = line.split('\t')
            yield tokens[self.column_index].strip()
        self._handle.close()


def create_iterator(type, entity_list):
    if type == 'txt':
        return TextIterator(entity_list)
    elif type == 'tsv':
        # TODO(oleg): currently hard-coded to the first column index.
        return TsvIterator(entity_list, column_index=0)
    elif type == 'url':
        return UrlIterator(entity_list)
    else:
        raise ValueError('Unsupported iterator type: {}'.format(type))


def gen_rand_metadata():
    s = 'abc 123 ghi j#@ m$o,.?'
    l = list(s)
    shuffle(l)
    return ''.join(l)


def gen_rand_index(output, metadata_fn, dim, doc_count):
    """ Generate random sptag index.

    format:
    <text-0>\t<v0>,...,<v-dim-1>\n
    ...
    <text-n>\t<v0>,...,<v-dim-1>\n
    """
    with open(output, 'w') as f:
        for i in range(doc_count):
            f.write(metadata_fn())
            f.write('\t')
            f.write('%f' % random())
            for n in range(dim - 1):
                f.write('|')
                f.write('%f' % random())
            f.write('\n')
    return doc_count


def write_record(p_out, p_phrases, p_vectors, p_dim):
    """ Write record (<phrase>\t<vector>\n) to a file. """
    for i, v in enumerate(p_vectors):
        p_out.write(p_phrases[i])
        p_out.write('\t')
        assert v.size > 0 and v.size == p_dim, 'Embedding dimension does not match. Expected:{}. Actual:{}'.format(p_dim, v.size)
        value = '|'.join([repr(a) for a in v])
        p_out.write(value)
        p_out.write('\n')


def gen_embedding_index(p_output, p_doc_iter, p_dim, p_encoder, p_batch_size=100):
    """ Generate sptag index from document list

    format:
    <text-0>\t<v0>,...,<v-p_dim-1>\n
    ...
    <text-n>\t<v0>,...,<v-p_dim-1>\n
    """
    phrases = []
    count = 0
    with open(p_output, 'w') as f:
        start = time.time()
        for phrase in p_doc_iter.next():
            if phrase == '' or len(phrase) == 0:
                continue
            phrases.append(phrase)
            if len(phrases) < p_batch_size:
                continue
            count += len(phrases)
            vectors = p_encoder.batch_encode(phrases)
            assert len(vectors) == len(phrases)
            write_record(f, phrases, vectors, p_dim)
            elapsed_secs = time.time() - start
            info('Progress: %d docs. Elapsed: %.3f s. Rate: %.2f dps ...' % (count, elapsed_secs, len(phrases)/elapsed_secs))
            vectors = []
            phrases = []
            start = time.time()

        if len(phrases) > 0:
            count += len(phrases)
            start = time.time()
            info('Indexing remaining {} docs'.format(len(phrases)))
            vectors = p_encoder.batch_encode(phrases)
            assert len(vectors) == len(phrases)
            write_record(f, phrases, vectors, p_dim)
            elapsed_secs = time.time() - start
            info('Progress: %d docs. Elapsed: %.3f s. Rate: %.2f dps ...' % (count, elapsed_secs, len(phrases)/elapsed_secs))
            vectors = []
            phrases = []
    return count


def batch_index(entity_list, batch_size, doc_count, index_name, dimension, random_index, encoder_config, output_dir,
                iterator_type):
    """ Create batch index (offline).

    --entity-list: list of entities to be indexed, it can be plain-text file with list of "sentences", or http://image.url
    --batch-size: the number of batch requests made to the encoder
    --doc-count: [only applies when --random-index specified], number of docs to generate.
    --index-name: name of the output index (a bundled of .fvec, .caption, and .em)
    --dimension: dimension of each vector embedding per entity
    --random-index: if True, generate random index
    --encoder-config: json config for instantiating encoder.
        Check: https://github.com/vasilynikita/hawking/tree/master/configs for samples.
    """
    if not random_index:
        assert entity_list is not None, "When --random-index is False, --entity-list argument is mandatory."
    dimension = int(dimension)

    embedding_output_path = '{}.em'.format(os.path.join(output_dir, index_name))
    start = time.time()
    if random_index:
        info('Generate random embedding ...')
        total_entity_count = gen_rand_index(embedding_output_path, gen_rand_metadata, dimension, doc_count)
    else:
        info('Generate embedding file from:`{}`...'.format(entity_list))
        entity_iter = create_iterator(iterator_type, entity_list)
        info('Encoder Config:{}'.format(encoder_config))
        if not isinstance(encoder_config, dict):
            with open(encoder_config, 'r') as f:
                encoder_config = json.load(f)
        encoder = create_encoder(config=encoder_config)
        if encoder_config['entity_type'] == 'text':
            total_entity_count = gen_embedding_index(embedding_output_path, entity_iter, dimension, encoder, batch_size)
        elif encoder_config['entity_type'] == 'image':
            total_entity_count = gen_embedding_index(embedding_output_path, entity_iter, dimension, encoder, batch_size)
        else:
            raise ValueError('-t {} is not supported!'.format(encoder_config['entity_type']))
    info('Completed building embedding file.')
    info(' Embedding    : %s' % embedding_output_path)
    info(' Total #docs  : %d' % total_entity_count)
    info(' Elapsed time : %.3f secs' % (time.time() - start))
    info(' Batch size   : %d' % batch_size)

    # Build faiss index from the generated embedding.
    # Building faiss index is typically much cheaper than running sentence encoding,
    # here we make an arbitrary assumption that we can batch it at ~20x.
    fvec_file_path = '{}.fvec'.format(os.path.join(output_dir, index_name))
    build_index(embedding_output_path, 20 * batch_size, dimension, fvec_file_path, HNSW_M=48)
    info('Completed building index file.')
