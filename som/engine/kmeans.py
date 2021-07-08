import os
from sklearn.cluster import KMeans
from gensim.models import KeyedVectors
from collections import defaultdict
import numpy as np
import random

from sklearn.decomposition import PCA


class Som:
    def __init__(self):
        vec_file = os.environ['VECTOR_DATA']
        self._wv = KeyedVectors.load_word2vec_format(vec_file, binary=True)

    def build(self, words, n_clusters):
        Y = [w for w in words if w in self._wv]
        X = [self._wv[y] / np.linalg.norm(self._wv[y]) for y in Y]

        pca = PCA(n_components=0.95) 
        X = pca.fit_transform(X)

        kmeans_model = KMeans(n_clusters=n_clusters, verbose=1, random_state=42, n_jobs=-1)
        kmeans_model.fit(X)

        cluster_labels = kmeans_model.labels_
        cluster_to_words = defaultdict(list)
        for cluster_id, word in zip(cluster_labels, Y):
            cluster_to_words[cluster_id].append(word)
        word_to_cluster = {words[i]:cluster_labels[i] for i in range(len(words))}
        return cluster_to_words, word_to_cluster

if __name__ == '__main__':
    som = Som()
    words = [
        'トマト', 
        'きゅうり', 
        '牛肉', 
        '豚肉', 
        '納豆', 
        '大豆', 
        '枝豆', 
        'ビール', 
        '緑茶', 
        'コーヒー', 
        '紅茶', 
        'すいか', 
        'メロン', 
        'たまねぎ', 
        '羊肉', 
        'パン', 
        ]

    k = 2
    while True:
        ctw, wtc = som.build(words, k)

        targets = [w for w in words if len(ctw[wtc[w]]) > 2]
        if len(targets) == 0:
            break
        wa = random.choice(targets)
        ca = wtc[wa]
        wb = random.choice([w for w in ctw[ca] if w != wa])
        while True:
            ans = input('Are {} and {} in same category? (y/n/end)'.format(wa, wb))
            if ans == 'y':
                break
            if ans == 'n':
                k += 1
                break; 
            if ans == 'end':
                break; 
        if ans == 'end':
            break; 
    for k in ctw:
        print('{}: {}'.format(k, ctw[k]))
