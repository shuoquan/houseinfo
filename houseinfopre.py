import pymysql
import numpy
import  json
import pandas  as pd
from pandas import Series,DataFrame
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
connection,cursor=conn_db()
# roomend=['1',2,3]
sql="select * from sechousedisposed"
cursor.execute(sql)
# sql="select * from sechousedisposed where 室=2"
# cursor.execute(sql)
data=cursor.fetchall()
jsondata = {"name": [i[0] for i in data],
            "region": [i[1] for i in data],
            "place": [i[2] for i in data],
            "room": [i[3] for i in data],
            "living": [i[4] for i in data],
            "kitchen": [i[5] for i in data],
            "bath": [i[6] for i in data],
            "area": [i[7] for i in data],
            "avgprice": [i[8] for i in data],
            "total": [i[9] for i in data],
            "direction": [i[10] for i in data],
            "house": [i[11] for i in data],
            "height": [i[12] for i in data],
            "decoration": [i[13] for i in data],
            "href": [i[14] for i in data],
            }
print(jsondata)
frame = DataFrame(jsondata)
newdata={"name": [i for i in frame['name']],
            # "region": frame['region'],
            # "place": frame['place'],
            # "room": frame['room'],
            # "living": frame['living'],
            # "kitchen": frame['kitchen'],
            # "bath": frame['bath'],
            # "area": frame['area'],
            # "avgprice": frame['avgprice'],
            # "total": frame['total'],
            # "direction": frame['direction'],
            # "house": frame['house'],
            # "height": frame['height'],
            # "decoration": frame['decoration'],
            # "href": frame['href'],
            }
print(newdata)
# jsondata = {"name": [i[0] for i in data],
#             "region": [i[1] for i in data],
#             "place": [i[2] for i in data],
#             "room": [i[3] for i in data],
#             "living": [i[4] for i in data],
#             "kitchen": [i[5] for i in data],
#             "bath": [i[6] for i in data],
#             "area": [i[7] for i in data],
#             "avgprice": [i[8] for i in data],
#             "total": [i[9] for i in data],
#             "direction": [i[10] for i in data],
#             "house": [i[11] for i in data],
#             "height": [i[12] for i in data],
#             "decoration": [i[13] for i in data],
#             "href": [i[14] for i in data],
#             }
# s=json.dumps(jsondata)
# newdata=json.parse(s)

# print(houseinfo)
# df=pd.read_sql(sql=sql,con=connection)
# print(df)