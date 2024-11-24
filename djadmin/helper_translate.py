import re

import psycopg2
import html2text as ht
import markdown2
from cfg import DB_INFO
from bs4 import BeautifulSoup

conn = psycopg2.connect(database=DB_INFO['NAME'], user=DB_INFO['USER'], password=DB_INFO['PASSWORD'],
                        host=DB_INFO['HOST'], port=DB_INFO['PORT'])

cursor = conn.cursor()


def htmlToMarkDown(html):
    text_maker = ht.HTML2Text()
    text_maker.bypass_tables = False
    text = text_maker.handle(html)
    return text


def main():
    query = "select id,cnt_md,cnt_html from crawldocumenten"
    cursor.execute(query)

    recs = cursor.fetchall()

    for rec in recs:
        # 创建Markdown对象并设置相关选项（可根据需求自定义）
        md = markdown2.Markdown(extras=['fenced-code-blocks'])

        # 调用convert()函数将Markdown转换为HTML
        html_content = md.convert(rec[1])
        # 创建Beautiful Soup对象来处理HTML内容
        soup = BeautifulSoup(html_content, 'html.parser')

        # 提取所有段落标签并进行翻译
        paragraphs = soup.findAll('p')
        for p in paragraphs:
            translated_text = translate(p.get_text())
            p.string = translated_text

        # 提取所有标题并进行翻译
        title_arr = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        for tit in title_arr:
            level_titles = soup.find_all(tit)
            for t in level_titles:
                translated_text = translate(t.get_text())
                t.string = translated_text

        # 查找所有包含<b>或</b>标签的元素
        bold_elements = soup.findAll(['b', 'strong'])
        for element in bold_elements:
            # print(element)
            translated_text = translate(element.get_text())
            element.string = '**' + translated_text + '**'

        # 遍历所有列表并并进行翻译
        lists = soup.find_all(['ul', 'ol'])
        for list in lists:
            for item in list.find_all('li'):
                translated_text = translate(item.get_text())
                item.string = translated_text

        # # 通过CSS选择器或XPath表达式查询所需的元素
        # code_elements = soup.select("pre")  # 根据实际情况修改选择器
        #
        # # 输出结果
        # for element in code_elements:
        #     element.string=element.text

        all_con = htmlToMarkDown(str(soup))

        sql = "UPDATE crawldocumenten SET cnt_md_trans = %s WHERE id = %s"
        values = (all_con, rec[0])
        cursor.execute(sql, values)
        conn.commit()


def translate(text):
    # todo:翻译处理


    # from translate import Translator
    # translator2 = Translator(from_lang="english", to_lang="chinese")
    # try:
    #     translation = translator2.translate(text)
    #     print(translation)
    #     return translation
    # except:
    #     return text

    return f"0{text}0"


if __name__ == '__main__':
    main()
