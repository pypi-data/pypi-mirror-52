
texts = [['human', 'interface', 'computer'],
['survey', 'user', 'computer', 'system', 'response', 'time'],
['eps', 'user', 'interface', 'system'],
['system', 'human', 'system', 'eps'],
['user', 'response', 'time'],
['trees'],
['graph', 'trees'],
['graph', 'minors', 'trees'],
['graph', 'minors', 'survey']]

from gensim import corpora
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
print(corpus[0]) # [(0, 1), (1, 1), (2, 1)]


from gensim import models
tfidf = models.TfidfModel(corpus)

doc_bow = [(0,1), (1,1)]
print(tfidf[doc_bow])

tfidf.save("./model.tfidf")
tfidf = models.TfidfModel.load("./model.tfidf")

