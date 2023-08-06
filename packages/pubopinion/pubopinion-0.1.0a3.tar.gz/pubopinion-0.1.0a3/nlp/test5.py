import jieba

for line in file.readlines():
    words = jieba.cut(line)
    for word in words:
        # print(word)
        if word not in stopword:
            output.write(word + " ")


def open_file():
    corpus = []
    token_path = "res_title_news.txt"
    try:

        with open(token_path, 'r', encoding="utf-8") as t:
            for line in t.readlines():
                corpus.append(line.strip())
        import gensim

        sentences = gensim.models.doc2vec.TaggedLineDocument(token_path)
        model = gensim.models.Doc2Vec(sentences, dm=1, size=200, window=10)
        model.train(sentences, total_examples=model.corpus_count, epochs=100)
        model.save('res_title_news_w2c.txt')
        out = open('res_title_news_vector.txt', 'w')
        for idx, docvec in enumerate(model.docvecs):
            for value in docvec:
                out.write(str(value) + ' ')
            out.write('\n')
    except Exception as e:
        print(e)


open_file()
