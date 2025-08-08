'''
逐行分词
'''

import re

import jieba
import jieba.posseg as pseg

file_userdict = 'def_userdict.txt'
jieba.load_userdict(file_userdict)


# 创建停用词list
def stopwordslist(filepath):
    stopwords = [
        line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()
    ]
    return stopwords


# 对句子进行分词
def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('def_stopword.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr


inputs = open('地球大数据元数据0906.csv', 'r', encoding='utf-8')
outputs = open('xx_fenci.txt', 'w', encoding='utf-8')

for line in inputs:
    r1 = (
        '[a-zA-Z0-9’!"#$%&\'()*+,-./:：;；|<=>?@，—。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    )
    line_seg = re.sub(r1, '', line)
    # line_seg = re.sub('[\d]', '', line)
    # line_seg2 = re.sub('[a-zA-Z]', '', line_seg)
    line_seg1 = seg_sentence(line_seg)  # 这里的返回值是字符串

    outputs.write(line_seg1 + '\n')

outputs.close()
inputs.close()
