import requests
from lxml import etree
import time
from datetime import datetime
import sys
 
 
#定义请求函数
def get_html(url,headers):
    response = requests.get(url , headers=headers)
    return response.text
 
 
#定义解析函数
def resolve_html(content):
    html = etree.HTML(content);
    return html
 
 
#定义主函数
def start():
   print("脚本运行时间：",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"———— ———— ——— ——— ——— ——— ——— ——— ———— ————")
   page_list = 2
   for p in range(page_list):
     domain = 'https://blog.csdn.net/woaidouya123/article/list/'+str(p+1)
     print(domain)
     headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',}
     try:
      content = get_html(domain,headers)
      pages = resolve_html(content).xpath('//*[@id="articleMeList-blog"]/div[2]/div/h4/a/@href')
      print(pages)
      for page in pages:
       page_content = get_html(page,headers)
       time.sleep(3)
       html = resolve_html(page_content)
       title = html.xpath('//*[@id="mainBox"]/main/div[1]/div/div/div[1]/h1')[0].text
       print(title,end=",")
     except:
      print("Unexpected error:", sys.exc_info()[0])

if __name__ == '__main__':
    start()
   
   
