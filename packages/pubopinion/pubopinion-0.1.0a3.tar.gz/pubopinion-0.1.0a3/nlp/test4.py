#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 18:31:11 2018

@author: luogan
"""

import jieba
import re
from gensim.models import word2vec
import multiprocessing
import gensim
import numpy as  np
import pandas as pd
import collections
import pandas


def segment_text(source_corpus, train_corpus, coding, punctuation):
    '''
    切词,去除标点符号
    :param source_corpus: 原始语料
    :param train_corpus: 切词语料
    :param coding: 文件编码
    :param punctuation: 去除的标点符号
    :return:
    '''
    with open(source_corpus, 'r', encoding=coding) as f, open(train_corpus, 'w', encoding=coding) as w:
        for line in f:
            # 去除标点符号
            line = re.sub('[{0}]+'.format(punctuation), '', line.strip())
            # 切词
            words = jieba.cut(line)
            w.write(' '.join(words))


# if __name__ == '__main__':


# 严格限制标点符号
strict_punctuation = '。，、＇：∶；?‘’“”〝〞ˆˇ﹕︰﹔﹖﹑·¨….¸;！´？！～—ˉ｜‖＂〃｀@﹫¡¿﹏﹋﹌︴々﹟#﹩$﹠&﹪%*﹡﹢﹦﹤‐￣¯―﹨ˆ˜﹍﹎+=<­­＿_-\ˇ~﹉﹊（）〈〉‹›﹛﹜『』〖〗［］《》〔〕{}「」【】︵︷︿︹︽_﹁﹃︻︶︸﹀︺︾ˉ﹂﹄︼'
# 简单限制标点符号
simple_punctuation = '’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
# 去除标点符号
punctuation = simple_punctuation + strict_punctuation

# 文件编码
coding = 'utf-8'

# coding ="gb18030"
# 原始语料
source_corpus_text = 'santi.txt'

# 是每个词的向量维度
size = 10
# 是词向量训练时的上下文扫描窗口大小，窗口为5就是考虑前5个词和后5个词
window = 5
# 设置最低频率，默认是5，如果一个词语在文档中出现的次数小于5，那么就会丢弃
min_count = 1
# 是训练的进程数，默认是当前运行机器的处理器核数。
workers = multiprocessing.cpu_count()
# 切词语料
train_corpus_text = 'words.txt'
# w2v模型文件
model_text = 'w2v_size_{0}.model'.format(size)

# 切词 @TODO 切词后注释
segment_text(source_corpus_text, train_corpus_text, coding, punctuation)

# w2v训练模型 @TODO 训练后注释
sentences = word2vec.Text8Corpus(train_corpus_text)
model = word2vec.Word2Vec(sentences=sentences, size=size, window=window, min_count=min_count, workers=workers)
model.save(model_text)

# 加载模型
model = gensim.models.Word2Vec.load(model_text)

g = open("words.txt", "r")  # 设置文件对象
std = g.read()  # 将txt文件的所有内容读入到字符串str中
g.close()  # 将文件关闭

cc = std.split(' ')

dd = []
kkl = dict()

'''
将每个词语向量化，并且append 在dd中，形成一个二维数组
并形成一个字典，index是序号，值是汉字
'''
for p in range(len(cc)):
    hk = cc[p]
    if hk in model:
        vec = list(model.wv[hk])
        dd.append(vec)
        kkl[p] = hk

# 将二维数组转化成numpy

dd1 = np.array(dd)

from sklearn.cluster import KMeans

estimator = KMeans(n_clusters=100)  # 构造聚类器
estimator.fit(dd1)  # 聚类
label_pred = estimator.labels_  # 获取聚类标签

# index 是某条向量的序号，值是分类号
index1 = list(range(len(dd1)))
vc = pd.Series(label_pred, index=index1)

aa = collections.Counter(label_pred)
v = pandas.Series(aa)
v1 = v.sort_values(ascending=False)

for n in range(10):
    vc1 = vc[vc == v1.index[n]]
    vindex = list(vc1.index)

    kkp = pd.Series(kkl)

    print('第', n, '类的前10个数据')

    ffg = kkp[vindex][:10]
    ffg1 = list(set(ffg))

    print(ffg1)