import os
from gensim.models import KeyedVectors


if __name__ == '__main__':
    vec_file = os.environ['VECTOR_DATA']
    wv = KeyedVectors.load_word2vec_format(vec_file, binary=True)
    while True:
        word = input("word: ")
        if word.strip() == "":
            break
        results = wv.most_similar(positive=[word])
        for result in results:
            print(result)