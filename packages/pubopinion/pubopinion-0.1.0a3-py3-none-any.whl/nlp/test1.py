from gensim import corpora
import jieba
documents = ['工业互联网平台的核心技术是什么',
            '工业现场生产过程优化场景有哪些']
def word_cut(doc):
    seg = [jieba.lcut(w) for w in doc]
    return seg

texts= word_cut(documents)

##为语料库中出现的所有单词分配了一个唯一的整数id
dictionary = corpora.Dictionary(texts)
dictionary.token2id
bow_corpus = [dictionary.doc2bow(text) for text in texts]
bow_corpus

from gensim import models
# train the model
tfidf = models.TfidfModel(bow_corpus)

def StopWordList(filepath):
    wlst = [w.strip() for w in open(filepath, 'r', encoding='utf-8').readlines()]
    return wlst

stop_flags = ['x', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r']

def seg_sentence(sentence,stop_words):
    sentence_seged = jieba.cut(sentence.strip())
    # sentence_seged = set(sentence_seged)
    outstr = ''
    for word in sentence_seged:
        if word not in stop_words:
            if word != '\t':
                outstr += word
                outstr += ' '

    return outstr.split(' ')


 #1、将【文本集】生产【分词列表】
    texts = [seg_sentence(seg,stop_words) for seg in open(tpath,'r',encoding='utf8').readlines()]
#一、建立词袋模型
    #2、基于文件集建立【词典】，并提取词典特征数
    dictionary = corpora.Dictionary(texts)
    feature_cnt = len(dictionary.token2id.keys())
    #3、基于词典，将【分词列表集】转换为【稀疏向量集】，也就是【语料库】
    corpus = [dictionary.doc2bow(text) for text in texts]
#二、建立TF-IDF模型
    #4、使用“TF-TDF模型”处理【语料库】
    tfidf = models.TfidfModel(corpus)
#三构建一个query文本，利用词袋模型的字典将其映射到向量空间
    #5、同理，用词典把搜索词也转换为稀疏向量
    kw_vector = dictionary.doc2bow(seg_sentence(keyword,stop_words))
    #6、对稀疏向量建立索引
    index = similarities.SparseMatrixSimilarity(tfidf[corpus],num_features=feature_cnt)
    #7、相似的计算
    sim = index[tfidf[kw_vector]]
