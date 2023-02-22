import requests
import json
import time

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

baseUrl = "https://geo.datav.aliyun.com/areas_v3/bound/geojson?code="
saveDir = "./json/"
deep = 3

#保存
def save(content,name):
  with open(saveDir + name + '.json','wb') as f:
    f.write(content)
    f.close()

#获取数据
def getMap(adcode, name, level):
  if(level <= deep):
    res = ""
    try:
      res = requests.get(baseUrl + adcode + "_full", headers).content
      parseMap(res, level)
      save(res, name)
    except: 
      print(adcode, name, "no data")

#解析下一层级数据
def parseMap(res, level):
  regionList = json.loads(res)["features"]
  for region in regionList:
    print(region["properties"]["name"], region["properties"]["adcode"])
    getMap(str(region["properties"]["adcode"]), region["properties"]["name"], level+1)
    # time.sleep(1)

getMap("100000", "中国", 1)
