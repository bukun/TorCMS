from pathlib import Path
import jieba.analyse

import re


def test_if_az09(string):
    '''
    ^ 匹配一行的开头位置
    (?![0-9]+$) 该位置后面不全是数字
    (?![a-zA-Z]+$) 该位置后面不全是字母
    [0-9A-Za-z] {8,16} 由8-16位数字或这字母组成

    | 指明两项之间的一个选择（将两个匹配条件进行逻辑“或”（or）运算）
    $ 匹配行结尾位置

    注：(?!xxxx) 是正则表达式的负向零宽断言一种形式，标识预该位置后不是xxxx字符。
    ————————————————
    版权声明：本文为CSDN博主「Chery Qi」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
    原文链接：https://blog.csdn.net/cheryjava/article/details/107835123

    '''
    pattern = r'^[0-9A-Za-z]{2,24}$'
    pattern = r'^[0-9A-Za-z]{2,240}(?![0-9]+$)(?![a-zA-Z]+$)$'
    res = re.search(pattern, string)
    print(res)
    if res:
        return True
    else:
        return False



mask_arr = []
with open('./torcms_taginfo/doc/mask.txt') as fi:
    for cnt in fi.readlines():
        cnt = cnt.strip()
        if cnt:
            mask_arr.append(cnt)

the_inws = Path('./torcms_taginfo/code_wangjy')
for wfile in the_inws.rglob('def_mask*.txt'):
    print(wfile.resolve())
    with open(wfile) as fi:
        for cnt in fi.readlines():
            cnt = cnt.strip()
            if cnt:
                mask_arr.append(cnt)

mask_arr = set(mask_arr)
print(mask_arr)


def get_tag_by_title(post_data):
    '''
    根据标题返回标签列表。
    :param post_data:
    :return:
    '''
    # tags_arr = jieba.analyse.extract_tags(post_data['title'])
    raw_text = post_data['title'] + '。' + post_data['text']


    # TF-idf 关键词提取
    tags_arr = jieba.analyse.extract_tags(raw_text)

    # textrank 关键词提取
    # tags_arr = jieba.analyse.textrank(raw_text)
    print('-' * 40)
    print(tags_arr)

    out_tag = []

    for tag in tags_arr:
        if test_if_az09(tag):
            continue
        else:
            pass
        try:
            int(tag)
            continue
        except:
            pass
        try:
            float(tag)
            continue
        except:
            pass

        if tag in mask_arr:
            pass
        else:
            out_tag.append(tag)

    return out_tag

if __name__ == '__main__':
    print(test_if_az09('MODIS'))
    print(test_if_az09('10m'))
    print(test_if_az09('1000E'))
    print(test_if_az09('天地'))
    print(test_if_az09('免费Jupyter科学计算服务，OSGeo中国中心发布'))