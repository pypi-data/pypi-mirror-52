import jieba


file_encoding = 'UTF-8'

if __name__ == '__main__':
    jieba.suggest_freq('沙瑞金', True)
    jieba.suggest_freq('易学习', True)
    jieba.suggest_freq('王大路', True)
    jieba.suggest_freq('京州', True)
    with open('../resources/chinese/nlp_test0.txt', encoding='UTF-8') as f:
        document = f.read()
        document_cut = jieba.cut(document)
        # print(jieba_cut)
        result = ' '.join(document_cut)
        result.encode('utf-8')
        with open('../resources/chinese/nlp_test1.txt', mode='w') as f2:
            f2.write(result)
    f.close()
    f2.close()
    with open('../resources/chinese/nlp_test2.txt', encoding='UTF-8') as f:
        document = f.read()
        document_cut = jieba.cut(document)
        # print(jieba_cut)
        result = ' '.join(document_cut)
        result.encode('utf-8')
        with open('../resources/chinese/nlp_test3.txt', mode='w') as f2:
            f2.write(result)
    f.close()
    f2.close()

    # 引入停用词
    stpwrdpath = '../resources/stop_words/stop_words.txt'
    stpwrd_dic = open(stpwrdpath, 'rb')
    stpwrd_content = stpwrd_dic.read()
    # 将停用此表转为List
    stpwrdlst = stpwrd_content.splitlines()
    stpwrd_dic.close()

    with open('../resources/chinese/nlp_test1.txt') as f3:
        res1 = f3.read()
    print(res1)
    with open('../resources/chinese/nlp_test3.txt') as f4:
        res2 = f4.read()
    print(res2)

    from sklearn.feature_extractiont.text import TfidVectorizer
    corpus = [res1, res2]
    vector = TfidVectorizer(stop_words=stpwrdlst)
    tfidf = vector.fit_transform(corpus)
    print(tfidf)
    # from jpype import *
    #
    # startJVM(getDefaultJVMPath(), "-ea")
    # java.lang.System.out.println("Hello World")
    # shutdownJVM()