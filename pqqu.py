# coding: utf-8


from urllib import request
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
from whoosh.fields import *
from create_whoosh1 import *


###新闻类定义
class News(object):
    def __init__(self):
        self.url = None  # 该新闻对应的url
        self.topic = None  # 新闻标题
        self.date = None  # 新闻发布日期
        self.content = None  # 新闻的正文内容
        self.author = None  # 新闻作者


###如果url符合解析要求，则对该页面进行信息提取
def getNews(url):
    # 获取页面所有元素
    # print('*'*50)
    html = request.urlopen(url).read().decode('utf-8', 'ignore')
    # 解析
    soup = BeautifulSoup(html, 'html.parser')

    # 获取信息
    if not (soup.find('table', {'class': 'tgaozhengwen1'})): return
    # print('*' * 50)
    news = News()  # 建立新闻对象

    page = soup.find('table', {'class': 'tgaozhengwen1'})

    if not (page.find('span', {'class': 'tgaozhengwentxet'})): return
    # print('*' * 50)
    topic = page.find('span', {'class': 'tgaozhengwentxet'}).get_text()  # 新闻标题
    news.topic = topic
    # print('*' * 50)
    contents = soup.find('span', {'class': 'tgaozhengwen2'})
    if not (contents.find('span', {'id': 'textflag'})): return
    # print('*' * 50)
    main_content = contents.find('span', {'id': 'textflag'})  # 新闻正文内容

    content = ''

    for p in main_content.select('span'):
        content = content + p.get_text()
    # print('*' * 50)
    news.content = content

    news.url = url  # 新闻页面对应的url
    create_wh(news.topic, news.url, news.content)
    f.write(news.topic + '\n' + news.url + '\n' + news.content + '\n' + '\n')

    print('-' * 50)
    print('sucess')
    print('-' * 50)




##dfs算法遍历全站###
def dfs(url):
    global count
    print(url)

    pattern1 = 'http://www.jianzai\.gov\.cn//DRpublish\/[a-z0-9_\/\.]*$'  # 可以继续访问的url规则
    pattern2 = 'http://www.jianzai\.gov\.cn//DRpublish\/[a-z]{4}\/[0-9]{16}\.html$'  # 解析新闻信息的url规则

    # 该url访问过，则直接返回
    if url in visited:  return
    print(url)

    # 把该url添加进visited()
    visited.add(url)
    # print(visited)

    try:
        # 该url没有访问过的话，则继续解析操作

        req = request.Request(url, headers=head)
        # 传入创建好的Request对象
        response = request.urlopen(req)
        html = response.read().decode('utf-8', 'ignore')
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')
        # print(visited)
        if re.match(pattern2, url):
            getNews(url)
            # count += 1

        ####提取该页面其中所有的url####
        links = soup.findAll('a', href=re.compile(pattern1))
        for link in links:
            print(link['href'])
            if link['href'] not in visited:
                dfs(link['href'])
                # count += 1
    except URLError as e:
        print(e)
        return
    except HTTPError as e:
        print(e)
        return
        # print(count)
        # if count > 3: return


visited = set()  ##存储访问过的url

head = {}
# 写入User Agent信息
head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'

f = open('news.txt', 'a+', encoding='utf-8')

dfs('http://www.jianzai.gov.cn/DRpublish/')
