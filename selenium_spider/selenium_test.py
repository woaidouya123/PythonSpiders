from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from lxml import etree

#定义解析函数
def resolve_html(content):
    html = etree.HTML(content);
    return html

chrome_options = webdriver.ChromeOptions()
# 使用headless无界面浏览器模式
chrome_options.add_argument('--headless') #增加无界面选项
chrome_options.add_argument('--disable-gpu') #如果不加这个选项，有时定位会出现问题

# 启动浏览器，获取网页源代码
browser = webdriver.Chrome(chrome_options=chrome_options)
mainUrl = "https://www.xicidaili.com/wn/"
browser.get(mainUrl)
iplist = resolve_html(browser.page_source).xpath('//*[@id="ip_list"]/tbody/tr/td[2]/text()')
portlist = resolve_html(browser.page_source).xpath('//*[@id="ip_list"]/tbody/tr/td[3]/text()')
print(len(iplist),len(portlist))
res = []
for i in range(len(iplist)):
	res.append(iplist[i] +":"+ portlist[i])
print(res)
browser.quit()