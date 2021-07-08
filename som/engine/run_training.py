from gensim.models import word2vec
import logging
import sys
import time

if __name__ == '__main__':
    args = sys.argv
    training_file = args[1]
    out_vector = args[2]

    start = time.time()
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus(training_file)

    model = word2vec.Word2Vec(sentences, min_count=20, window=15)
    model.wv.save_word2vec_format(out_vector, binary=True)

    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
