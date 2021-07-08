import os
from gensim.models import KeyedVectors
import numpy as np

from somoclu import Somoclu
from sklearn.decomposition import PCA

import matplotlib

class Som:
    def __init__(self):
        vec_file = os.environ['VECTOR_DATA']
        self._wv = KeyedVectors.load_word2vec_format(vec_file, binary=True)
        matplotlib.rc('font', family='TakaoPGothic')

    def build(self, n_rows, n_cols, words):
        for word in words:
            print('{}: {}'.format(word, self._wv[word]))
        Y = [w for w in words if w in self._wv]
        X = [self._wv[y] / np.linalg.norm(self._wv[y]) for y in Y]

        # SOMに入れる前にPCAして計算コスト削減を測る
        pca = PCA(n_components=0.95) 
        X = pca.fit_transform(X)

        # SOMの定義
        som = Somoclu(n_rows=n_rows, n_columns=n_cols,
            initialization="pca", verbose=2)

        # 学習
        som.train(data=X, epochs=1000)

        # U-matrixをファイル出力
        som.view_umatrix(labels=Y, bestmatches=True,
            filename="umatrix.png")

    def sim(self, w0, w1):
        v0 = self._wv[w0]
        v1 = self._wv[w1]
        sim = np.dot(v0, v1) / (np.linalg.norm(v0) * np.linalg.norm(v1))
        return sim


    def sim_table(self, words, path):
        with open(path, 'w') as f:
            f.write('{}\t{}\n'.format('', '\t'.join([w1 for w1 in words])))
            for w0 in words:
                f.write('{}\t{}\n'.format(w0, '\t'.join([str(self.sim(w0, w1)) for w1 in words])))
            


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
    som.build(25, 25, words)
    som.sim_table(words, 'table.csv')
    
