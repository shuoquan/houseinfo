from django.test import TestCase

# Create your tests here.
# import pymysql
# def conn_db():  # 数据库连接函数
#     conn = pymysql.connect(
#         host='localhost',
#         user='root',
#         passwd='dsq18962365926',
#         db='houseinfo',
#         charset='utf8'
#     )
#     cur = conn.cursor()
#     return conn, cur
#
# def get_data(sql):
#     con, cur = conn_db()
#     cur.execute(sql)
#     results = cur.fetchall()
#     cur.close()
#     con.close()
#     return results
# Location="万科假日风景"
# renthousesql="select * from renthousedispose where 小区名称 like '%%%%%s%%%%'" % Location
# rentdata=get_data(renthousesql)
# print(len(rentdata))
from bs4 import BeautifulSoup
import requests as req
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36",
    'Connection': "keep-alive",
    'Referer': 'https://lianjia.com/'
}
url="http://127.0.0.1:8000/index/"
res = req.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
s=soup.select(".info")
print(soup)