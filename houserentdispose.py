import pymysql
import re
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
conn,cur=conn_db()
# sql="create table if not exists renthousedispose(小区名称 TEXT,区 TEXT,地 TEXT,室 TEXT,厅 TEXT,卫 TEXT,建筑面积 TEXT,月租 TEXT,房屋朝向 TEXT,楼层属性 TEXT,楼层高度 TEXT,网页链接 TEXT)"
sql="select * from renthoused"
cur.execute(sql)
results=cur.fetchall()
# print(results[0])
# print(re.findall("\d+",results[0][6].split()[1])[0])
for result in results:
  sql=sql="insert into renthousedispose(小区名称,区,地,室,厅,卫,建筑面积,月租,房屋朝向,楼层属性,楼层高度,网页链接)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(result[0],result[1].split('-')[0],result[1].split('-')[1],re.findall("\d+",result[2])[0],re.findall("\d+",result[2])[1],re.findall("\d+",result[2])[2],result[3].replace('㎡',''),result[4].replace('元/月','').strip(),result[5].split()[0],result[6].split()[0],re.findall("\d+",result[6].split()[1])[0],result[7])
  cur.execute(sql)
conn.commit()
conn.close()