import requests as req
from bs4 import BeautifulSoup
import pymysql

headers = {
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

def getallestate(url):
    res = req.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    renthouses = soup.find_all(class_="title")
    locationlist=[]
    for i in range(0,len(renthouses)-2):
        if(len(renthouses[i].find_all('a'))!=0):
            locationlist.append(renthouses[i].find_all('a')[0].text)
    urls=soup.find_all(class_="houseInfo")
    renturl=[]
    for url in urls:
        renturl.append(url.find_all('a')[1].get('href'))
    return locationlist,renturl

def getrenthouseinfo(location,url,con,cur):
    for i in range(0,len(url)):
        res = req.get(url[i], headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        pageurl = soup.find_all(class_="content__pg")
        if len(pageurl)!=0:
            pagetotal = pageurl[0].get("data-totalpage")
            dataurl = pageurl[0].get("data-url")
        urls = []
        domain = "https://sh.lianjia.com"
        urllist = []
        urlindexlist=[]
        placelist = []
        arealist = []
        directionlist =[]
        shapelist = []
        heightlist = []
        pricelist =[]
        if len(pagetotal)!=0:
            for m in range(1, int(pagetotal) + 1):
                subdomain = dataurl.replace("{page}", str(m))
                urllist.append(domain + subdomain)

        for suburl in urllist:
            resp = req.get(suburl, headers=headers)
            bs = BeautifulSoup(resp.text, 'html.parser')
            renthouseurls = bs.find_all(class_=["content__list--item--title", "twoline"])
            allarea=bs.find_all(class_="content__list--item--des")
            allprice=bs.find_all(class_="content__list--item-price")
            for j in range(0,len(allarea)):
                urlindex=domain+renthouseurls[j].find_all('a')[0].get('href')
                list=allarea[j].text.replace("\n","").strip().split("/")
                place=list[0].strip()
                area=list[1].strip()
                direction=list[2].strip()
                shape=list[3].strip()
                height=list[4].strip()
                price=allprice[j].text.strip()
                urlindexlist.append(urlindex)
                placelist.append(place)
                arealist.append(area)
                directionlist.append(direction)
                shapelist.append(shape)
                heightlist.append(height)
                pricelist.append(price)
        for k in range(0,len(placelist)):
            sql="insert into renthouse(小区名称,所在区域,房屋户型,建筑面积,月租,房屋朝向,所在楼层,网页链接)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (
                location[i],placelist[k],shapelist[k],arealist[k],pricelist[k],directionlist[k],heightlist[k],urlindexlist[k])
            cur.execute(sql)
            con.commit()


    # area = soup.find_all(class_="content__list--item--des")
    # price=soup.find_all(class_="content__list--item-price")
    # print(area[8].text.replace("\n","").strip().split("/"))
    # print(price[0].text.strip())
locationlist,renturl=getallestate("https://sh.lianjia.com/xiaoqu/")
# getrenthouseinfo("https://sh.lianjia.com/zufang/c5011000017872/")

conn,cur=conn_db()
getrenthouseinfo(locationlist,renturl,conn,cur)
conn.close()

# sql = "create table if not exists renthouse(小区名称 TEXT,所在区域 TEXT,房屋户型 TEXT,建筑面积 TEXT,月租 TEXT,房屋朝向 TEXT,所在楼层 TEXT,网页链接 TEXT)"
# cur.execute(sql)

