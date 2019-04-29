import random

import requests as req
from bs4 import BeautifulSoup
import time
from threading import Thread
from queue import Queue
import pymysql
headers = {
    # 'Host': "bj.lianjia.com",
    # 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    # 'Accept-Encoding': "gzip, deflate, sdch",
    # 'Accept-Language': "zh-CN,zh;q=0.8",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36",
    'Connection': "keep-alive",
    'Referer': 'https://lianjia.com/'
}
def conn_db():  #数据库连接函数
    conn=pymysql.connect(
        host='localhost',
        user='root',
        passwd='dsq18962365926',
        db='houseinfo',
        charset='utf8'
    )
    cur=conn.cursor()
    return conn,cur
class HouseSpider():
    def __init__(self,url,conndb,cur):
        super(HouseSpider,self).__init__()
        self.url=url
        self.conndb=conndb
        self.cur=cur


    def run(self):
        # houseurls=gethouseurls(self.url)
        # for houseurl in houseurls:
        #     self.getHouseInfo(self,houseurl,self.conndb,self.cur)
        self.getHouseInfo(self.url,self.conndb,self.cur)

    def getHouseInfo(self,url, conndb, cur):
        houseurls=gethouseurls(url)
        print(houseurls)
        for houseurl in houseurls:
            info = {}
            soup = BeautifulSoup(req.get(houseurl, headers=headers).text, "html.parser")
            # 得到小区名称，并记录到字典
            res = soup.select(".communityName")
            coumnityName = res[0].select(".info")[0].string
            info['小区名称'] = coumnityName
            # 得到小区所在区域，并记录到字典
            target = "所在区域"
            res = soup.select(".areaName")
            HouseLocation = res[0].text
            houseLocation = HouseLocation[len(target):]
            info['所在区域'] = houseLocation
            # 得到房屋户型，并记录到字典
            target = "房屋户型"
            res = soup.find(text=target).parent.parent
            Housetype = res.text
            housetype = Housetype[len(target):]
            info['房屋户型'] = housetype
            # 得到房屋建筑面积，并记录到字典
            target = "建筑面积"
            res = soup.find(text=target).parent.parent
            Housearea = res.text
            housearea = Housearea[len(target):]
            info['建筑面积'] = housearea
            # 得到房屋单价，并记录到字典
            res = soup.select(".unitPriceValue")[0]
            unitPriceValue = res.text
            info['单价'] = unitPriceValue
            # print(unitPriceValue)
            # 得到房屋总价，并记录到字典
            res = soup.select(".total")
            totalPrice = res[0].text
            info['总价'] = totalPrice + '万'
            # 得到房屋朝向，并记录到字典
            target = "房屋朝向"
            res = soup.find(text=target).parent.parent
            Housedirection = res.text
            housedirection = Housedirection[len(target):]
            info['房屋朝向'] = housedirection
            # 得到房屋所在楼层，并记录到字典
            target = "所在楼层"
            res = soup.find(text=target).parent.parent
            HouseLevel = res.text
            houseLevel = HouseLevel[len(target):]
            info['所在楼层'] = houseLevel
            # 得到房屋装修情况，并记录到字典
            target = "装修情况"
            res = soup.find(text=target).parent.parent
            HouseDecoration = res.text
            houseDecoration = HouseDecoration[len(target):]
            info['装修情况'] = houseDecoration
            # print(info)
      
            info['网页链接']=houseurl
            sql = "insert into sechouse(小区名称,所在区域,房屋户型,建筑面积,单价,总价,房屋朝向,所在楼层,装修情况,网页链接)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                info['小区名称'], info['所在区域'], info['房屋户型'], info['建筑面积'], info['单价'], info['总价'], info['房屋朝向'],
                info['所在楼层'],
                info['装修情况'],
            info['网页链接'])
            try:
                cur.execute(sql)
                conndb.commit()
            except:
                conndb.rollback()
            time.sleep(random.random())
            # sta=conndb.exe_update(cur,"insert into sechouse(小区名称,所在区域,房屋户型,建筑面积,单价,总价,房屋朝向,所在楼层,装修情况)"
            #                       "values('%s','%s','%s','%s','%s','%s','%s','%s','%s') "%
            #                       (info['小区名称'],info['所在区域'],info['房屋户型'],info['建筑面积'],info['单价'],info['总价'],info['房屋朝向'],info['所在楼层'],info['装修情况']))


def getAllurl(begin, end, domain):
    urlist = []
    if (begin <= end):
        for i in range(begin, end + 1):
             url = domain + 'ershoufang' + '/pg' + str(i)
             urlist.append(url)
    else:
        print("输入错误")
    return urlist
def gethouseurls(url):
    res = req.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    houses = soup.select(".title")
    houseurls = []  # houseurl列表用来记录当前页面下所有的房源链接
    for house in houses:
        if (house.get('href') != None):
            houseurls.append(house.get('href'))
    time.sleep(random.random())
    return houseurls
#
conn,cur=conn_db()
# sql = "create table if not exists sechouse(小区名称 TEXT,所在区域 TEXT,房屋户型 TEXT,建筑面积 TEXT,单价 TEXT,总价 TEXT,房屋朝向 TEXT,所在楼层 TEXT,装修情况 TEXT,网页链接 TEXT)"
# cur.execute(sql)
domain="https://sh.lianjia.com/"
urllist=getAllurl(91,100,domain)
for url in urllist:
    p=HouseSpider(url,conn,cur)
    p.run()

#     houseurls=gethouseurls(url)
#     for houseurl in houseurls:
#         getHouseInfo(houseurl,conn,cur)

conn.close()

# test_url="https://sh.lianjia.com/ershoufang/107100331119.html"
# getHouseInfo(test_url)

# url="https://sh.lianjia.com/ershoufang/rs/"
# urlist=getAllurl(1,2,"https://sh.lianjia.com/")
# print(urlist)

