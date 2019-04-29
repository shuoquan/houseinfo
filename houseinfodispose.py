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
db,cursor=conn_db()
# sql="create table if not exists sechousedisposed(小区名称 TEXT,区 TEXT,地 TEXT,室 TEXT,厅 TEXT,厨 TEXT,卫 TEXT,建筑面积 TEXT,单价 TEXT,总价 TEXT,房屋朝向 TEXT,楼层属性 TEXT,总楼层 TEXT,装修情况 TEXT,网页链接 TEXT)"
# cursor.execute(sql)
sql="select * from sechouse"
cursor.execute(sql)
results = cursor.fetchall()
for row in results:
#     # print(row[1].split()[1])
#     # sql = "insert into sechousedispose(小区名称,区,地,房屋户型,建筑面积,单价,总价,房屋朝向,楼层属性,总楼层,装修情况,网页链接)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
#     #     row[0], row[1].split()[0], row[1].split()[1], row[2], row[3], row[4], row[5], row[6], row[7],
#     #     row[8],row[9])
    sql = "insert into sechousedisposed(小区名称,区,地,室,厅,厨,卫,建筑面积,单价,总价,房屋朝向,楼层属性,总楼层,装修情况,网页链接)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
        row[0], row[1].split()[0], row[1].split()[1],re.findall("\d+",row[2])[0],re.findall("\d+",row[2])[1],re.findall("\d+",row[2])[2],re.findall("\d+",row[2])[3], row[3].replace('㎡', ''), row[4].replace('元/平米', ''),
        row[5].replace('万',''), row[6].split()[0], re.sub(u"\\(.*?\\)","",row[7]),re.findall("\d+",row[7])[0],
        row[8], row[9])
    cursor.execute(sql)
#     # print(re.findall("\d+",row[2]))
    db.commit()
# db.commit()
# try:
#     cursor.execute(sql)
#     results = cursor.fetchall()
#     for row in results:
#        # print(row[1].split()[1])
#        sql="insert into sechouse(小区名称,区,地,备注,房屋户型,建筑面积,单价,总价,房屋朝向,所在楼层,装修情况)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
#         row[0],row[1].split()[0],row[1].split()[1],row[1].split()[2],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
#        cursor.execute(sql)
#
# except:
#     print("error")
db.close()