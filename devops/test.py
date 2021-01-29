# -*- coding=utf-8 -*-

"""
     原始数据，用于建立模型
"""

import os
import sys
import nltk
from nltk import data

data.path.append("./devops/nltk_data/packages")
import jieba.analyse
from nltk.tokenize import word_tokenize
from nltk.stem.lancaster import LancasterStemmer

from gensim import corpora, models, similarities


def prepare_data():
    # 缩水版的courses，实际数据的格式应该为 课程名\t课程简介\t课程详情，并已去除html等干扰因素

    # courses = [
    #     u'中华人民共和国在线地图（1:1200万）',
    #     u'中华人民共和国在线地图',
    #     u'中国供水能力（1:2100万）在线地图',
    #     u'中国互联网分布在线地图',
    #     u'中国解放区分布（1949年）在线历史地图',
    #     u'中国地级市管县级市（截至1999年底）在线历史地图',
    #     u'中国直辖市、地级市管县分布（截至1999年底）在线历史地图',
    #     u'中国地市合并分布（截至1999年底）在线历史地图',
    #     u'中华人民共和国在线地图',
    #     u'The Dynamic Earth: A Course for Educators',
    #     u'Tiny Wings\tYou have always dreamed of flying - but your wings are tiny. Luckily the world is full of beautiful hills. Use the hills as jumps - slide down, flap your wings and fly! At least for a moment - until this annoying gravity brings you back down to earth. But the next hill is waiting for you already. Watch out for the night and fly as fast as you can. ',
    #     u'Angry Birds Free',
    #     u'没有\它很相似',
    #     u'没有\t它很相似',
    #     u'没有\t他很相似',
    #     u'没有\t他不很相似',
    #     u'没有',
    #     u'可以没有',
    #     u'也没有',
    #     u'有没有也不管',
    #     u'Angry Birds Stella',
    #     u'Flappy Wings - FREE\tFly into freedom!A parody of the #1 smash hit game!',
    #     u'没有一个',
    #     u'没有一个2',
    # ]
    #
    # # 只是为了最后的查看方便
    # # 实际的 courses_name = [course.split('\t')[0] for course in courses]
    # courses_name = courses
    # return courses_name

    filepath = './xx_title/0100/ch101_遥感_0111/0111.md'
    if os.path.exists(filepath):
        pass
    else:
        print('File not exists.')
        sys.exit(0)

    cnts = open(filepath).readlines()
    cnts = [x.strip().split('|')[1] for x in cnts]
    # print(cnts)
    return cnts


def pre_process_cn(courses, low_freq_filter=True):
    """
    预处理(easy_install nltk)

     简化的 中文+英文 预处理
        1.去掉停用词
        2.去掉标点符号
        3.处理为词干
        4.去掉低频词

    """
    texts_tokenized = []
    for document in courses:
        texts_tokenized_tmp = []
        for word in word_tokenize(document):
            texts_tokenized_tmp += jieba.analyse.extract_tags(word, 10)
        texts_tokenized.append(texts_tokenized_tmp)

    texts_filtered_stopwords = texts_tokenized

    # 去除标点符号
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    texts_filtered = [[word for word in document if not word in english_punctuations] for document in
                      texts_filtered_stopwords]

    # 词干化

    st = LancasterStemmer()
    texts_stemmed = [[st.stem(word) for word in docment] for docment in texts_filtered]

    # 去除过低频词
    if low_freq_filter:
        all_stems = sum(texts_stemmed, [])
        stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
        texts = [[stem for stem in text if stem not in stems_once] for text in texts_stemmed]
    else:
        texts = texts_stemmed
    return texts


def train_by_lsi(lib_texts):
    """
    引入gensim，正式开始处理(easy_install gensim)
        通过LSI模型的训练
    """

    # 为了能看到过程日志
    # import logging
    # logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    dictionary = corpora.Dictionary(lib_texts)
    corpus = [dictionary.doc2bow(text) for text in
              lib_texts]  # doc2bow(): 将collection words 转为词袋，用两元组(word_id, word_frequency)表示
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    # 拍脑袋的：训练topic数量为10的LSI模型
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)
    index = similarities.MatrixSimilarity(lsi[corpus])  # index 是 gensim.similarities.docsim.MatrixSimilarity 实例

    return (index, dictionary, lsi)


if __name__ == '__main__':
    courses = prepare_data()

    lib_texts = pre_process_cn(courses)

    # 库建立完成 -- 这部分可能数据很大，可以预先处理好，存储起来
    (index, dictionary, lsi) = train_by_lsi(lib_texts)


    for rec in courses:
        # 要处理的对象登场
        print('-' * 40)
        print(rec)
        target_courses = [rec]
        target_text = pre_process_cn(target_courses, low_freq_filter=False)

        """
        对具体对象相似度匹配
        """

        # 选择一个基准数据
        ml_course = target_text[0]

        # 词袋处理
        ml_bow = dictionary.doc2bow(ml_course)

        # 在上面选择的模型数据 lsi 中，计算其他数据与其的相似度
        ml_lsi = lsi[ml_bow]  # ml_lsi 形式如 (topic_id, topic_value)
        sims = index[ml_lsi]  # sims 是最终结果了， index[xxx] 调用内置方法 __getitem__() 来计算ml_lsi

        # 排序，为输出方便
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])

        # 查看结果
        print(sort_sims[0:10])  # 看下前10个最相似的，第一个是基准数据自身

        for ii in range(10):
            print(ii, courses[sort_sims[ii][0]])  # 看下实际最相似的数据叫什么
