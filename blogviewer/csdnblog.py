import requests
from lxml import etree
import time
import sys
 
 
#定义请求函数
def get_html(url,headers):
    response = requests.get(url , headers)
    return response.content
 
 
#定义解析函数
def resolve_html(content):
    html = etree.HTML(content);
    return html
 
 
#定义主函数
def start():
   domain = 'https://blog.csdn.net/woaidouya123'
   headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'}
   try:
    content = get_html(domain,headers)
    pages = resolve_html(content).xpath('//*[@id="mainBox"]/main/div[2]/div/h4/a/@href')
    for page in pages:
     page_content = get_html(page,headers)
     time.sleep(3)
     html = resolve_html(page_content)
     title = html.xpath('//*[@id="mainBox"]/main/div[1]/div/div/div[1]/h1')[0].text
     print(title,end=",")
   except:
    print("Unexpected error:", sys.exc_info()[0])
   
   
