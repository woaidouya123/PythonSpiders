import requests
from lxml import etree
import time
import re
import shutil
import os

#定义请求函数
def get_html(url,headers):
    response = requests.get(url , headers)
    r = response.content.decode('gbk', 'ignore')
    return r

#定义解析函数
def resolve_html(content):
    html = etree.HTML(content);
    return html

#保存
def save(url,name):
  r=requests.get(url, headers=headers)
  with open(saveDir + name + '.txt','wb') as f:
    f.write(r.content)
    f.close()

#转移文件
def transStorage(name='test.txt'):
    save_path = saveDir + name + '.txt'
    print('transfering', save_path, transDir)
    try:
      shutil.move(save_path, transDir)
    except:
      print('transfer error')

#获取排行目录
def getRankList(category, pages):
  for page in range(pages):
    dirurl = '/top/' + category + '_' + str(page + 1) + ".html"
    print(domain+dirurl)
    content = get_html(domain+dirurl, headers)
    articles = resolve_html(content).xpath('//table/tr/td[1]/a/text()')
    urls = resolve_html(content).xpath('//table//tr/td[1]/a/@href')
    print(articles)
    for i in range(len(articles)):
      if articles[i] + '.txt' not in filelist:
        print('正在爬取书籍', articles[i], urls[i])
        downloadUrl = '/down/' + str(re.search(r'(\d+)', urls[i]).group())
        print(domain + downloadUrl)
        save(domain + downloadUrl, articles[i])
        transStorage(articles[i])
        time.sleep(10)
      else:
        print('skip', articles[i])

domain = 'http://www.ltxswo.us'
saveDir = './book/'
transDir = './trans'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
filelist = os.listdir(transDir)

#定义主函数
def main():
  categorys = ['allvisit']
  for cate in categorys:
    getRankList(cate, 1)
    time.sleep(3)

if __name__ == '__main__':
  main()

