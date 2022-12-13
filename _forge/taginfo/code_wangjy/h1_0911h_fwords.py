import re
with open(r'xx_fenci.txt',encoding='utf-8') as f:
    line = f.read().strip()
    words = re.split(r"[\s\n]", line)
   # print(result)



def deal_with_words(words):
    '''统计词频'''
    dic = {}
    for i in words:
        if len(i) > 1:
            dic[i] = words.count(i)
    words_list = list(dic.items())
    words_list.sort(key= lambda x:x[1], reverse=True)
    print ('字符\t词频')
    print ('=============')
    for i in range(200):
        word, count = words_list[i]
        print("{0:<10}{1:>5}".format(word, count))

deal_with_words(words)
