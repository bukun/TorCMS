#对无实意的高频词转化成stopwords的格式

f1 = open('无实意高频词.txt','r', encoding='utf-8')
f2 = open('txt-huanghang.txt','w', encoding='utf-8')
for line in f1:
    f2.write(line + '\n')

f2.close()
f1.close()