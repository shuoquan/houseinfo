import pymysql
from pyecharts import Bar
from pyecharts import Pie
import json

from pyecharts.engine import create_default_environment
from pyecharts import Map
env=create_default_environment("html")
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
db,cursor=conn_db()
sql="select 区, round(avg(单价)) as 均价, count(*) as 总数 from sechousedispose group by 区"
cursor.execute(sql)
avg_price=cursor.fetchall()
print(avg_price)
jsondata={"area":[i[0] for i in avg_price],
          "avgprice":[i[1] for i in avg_price ],
          "total":[i[2] for i in avg_price]}
print(jsondata)
# print(type(avg_price))


# print(avg_price)
# price=list(tuple(avg_price))
# area_list=[]
# avgprice_list=[]
# for i in price:
#     area_list.append(i[0])
#     avgprice_list.append(i[1])
# bar=Bar("区域单位均价")
# bar.add("区域均价(元/平米 )",area_list,avgprice_list,bar_category_gap='20%')
# bar.render('./housetotal.html')
# sql="select 区, count(*) as 二手房总数 from sechousedispose group by 区"
# cursor.execute(sql)
# sechousetotal=cursor.fetchall()
# area_list=[]
# housetotal=[]
# for i in sechousetotal:
#     area_list.append(i[0])
#     housetotal.append(i[1])
# pie=Pie("二手房源地区分布",title_pos='right')
# pie.add("",area_list,housetotal,is_label_show=True)
# pie.render("./housetoal.html")
