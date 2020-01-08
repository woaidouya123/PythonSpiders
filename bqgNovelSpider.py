import requests
from lxml import etree
import time
 
 
#定义请求函数
def get_html(url,headers):
    response = requests.get(url , headers)
    return response.content
 
 
#定义解析函数
def resolve_html(content):
    html = etree.HTML(content);
    return html

#写入txt
def save(novel):
    save_path = 'hello.txt'
    fp = open(save_path , 'a',encoding='utf-8',newline='\n')
    fp.write(novel)
    fp.close()
 
 
#定义主函数
def main():
   domain = 'http://www.xbiquge.la'
   dirurl = '/1/1690/'
   headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'}
   content = get_html(domain+dirurl,headers)
   pages = resolve_html(content).xpath('//*[@id="list"]/dl/dd/a/@href')
   for page in pages:
    page_content = get_html(domain+page,headers)
    time.sleep(1)
    html = resolve_html(page_content)
    title = html.xpath('//*[@class="bookname"]/h1')[0].text
    article = html.xpath('//*[@id="content"]/text()')
    print(title)
    save(title + '\n')
    for part in article:
      save(part)
main()
   
