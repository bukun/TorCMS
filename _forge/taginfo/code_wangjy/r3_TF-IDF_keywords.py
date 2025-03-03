import jieba.analyse

# f = open(r'C:\Users\王敬悦\Desktop\111.txt', encoding='utf-8')

# f = open(r'xx_fenci.txt', encoding='utf-8')
f = open('地球大数据元数据0906.csv', encoding='utf-8')
sentence = f.read()

# 基于 TF-IDF提取关键字
keywords = jieba.analyse.extract_tags(
    sentence, topK=1000, withWeight=True, allowPOS=('n', 'nr', 'ns')
)
# print(type(keywords))

with open('xx_tfidf1000.txt', 'w') as fo:
    for item in keywords:
        print(item[0], item[1])
        fo.write(item[0] + '\n')

keywords = jieba.analyse.extract_tags(
    sentence, topK=10000, withWeight=True, allowPOS=('n', 'nr', 'ns')
)
with open('xx_tfidf10000.txt', 'w') as fo:
    for item in keywords:
        print(item[0], item[1])
        fo.write(item[0] + '\n')
