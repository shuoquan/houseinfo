from django.shortcuts import render
import pymysql
import re
import json
from pyecharts import Bar
from pyecharts import Pie
# Create your views here.
from django.http import HttpResponse, JsonResponse
import pandas as pd
from pandas import Series,DataFrame

def index(request):
    return render(request, 'sechouse/../templates/index.html')
    # return render(request, 'sechouse/../templates/test.html')
def renthouse(request):
    return render(request,'sechouse/../templates/renthouse.html')
def sechouse(request):
    return render(request,'sechouse/../templates/sechouse.html')
def conn_db():  # 数据库连接函数
    conn = pymysql.connect(
        host='localhost',
        user='root',
        passwd='dsq18962365926',
        db='houseinfo',
        charset='utf8'
    )
    cur = conn.cursor()
    return conn, cur


def info(request):
    sql = "select 区, round(avg(单价)) as avg_price, count(*) as total from sechousedisposed group by 区"
    m_data = get_data(sql)
    return render(request, 'sechouse/../templates/houseinfo.html')


def get_data(sql):
    con, cur = conn_db()
    cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    con.close()
    return results


def showtable(request):
    sql = "select 区, round(avg(单价)) as avg_price, count(*) as total from sechousedisposed group by 区"
    data = get_data(sql)
    jsondata = {"area": [i[0] for i in data],
                "avg_price": [i[1] for i in data],
                "total": [i[2] for i in data]}
    return JsonResponse(jsondata)


# def showallhouse(request):
#     sql="select * from sechousedispose "
#     data=get_data(sql)
#

def showsecinfo(request):
    # area = request.GET.get('location')
    # sql = "select * from sechousedisposed"
    # data = get_data(sql)
    # return render(request, 'sechouse/../templates/sechouseinfo.html', {'sechouseinfo': data})
    # if request.is_ajax():
    #     sql = "select * from sechousedisposed"
    #     data = get_data(sql)
    #     return render(request, 'sechouse/../templates/sechouseinfo.html', {'sechouseinfo': data})
    # else:
    return render(request, 'sechouse/../templates/sechouseinfo.html')
def housenum(request):
    location=request.GET.get('locationname')
    Location = re.sub(u"\\(.*?\\)", "", location)
    renthousesql="select * from renthousedispose where 小区名称 like '%%%%%s%%%%'" % Location
    rentdata=get_data(renthousesql)
    sechousesql="select * from sechousedisposed where 小区名称 like '%%%%%s%%%%'" % Location
    sechousedata=get_data(sechousesql)
    data={
        "rentnum":len(rentdata),
        "sechousenum":len(sechousedata),
    }
    return JsonResponse(data)
def filter(request):
    regionend = request.GET.get('Region'),
    roomend = request.GET.get('Room'),
    livingend = request.GET.get('Living'),
    bathend = request.GET.get('Bath'),
    directionend = request.GET.get('Direction'),
    houseend = request.GET.get('House'),
    heightend = request.GET.get('Height'),
    decorationend = request.GET.get('Decoration'),
    areaminend = request.GET.get('Areamin'),
    areamaxend = request.GET.get('Areamax'),
    avgminend = request.GET.get('Avgmin'),
    avgmaxend = request.GET.get('Avgmax'),
    totalminend = request.GET.get('Totalmin'),
    totalmaxend = request.GET.get('Totalmax'),
    sql = "select * from sechousedisposed"
    # sql = "select * from sechousedisposed where 室='" + roomend[0] + "'"
    data = get_data(sql)
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
    frame= DataFrame(jsondata)
    if regionend[0]!='选项':
        frame=frame[frame['region']==regionend[0]]
    if roomend[0]!='选项':
        if roomend[0]=='4':
            frame=frame[frame['room']>'3']
        else:
            frame=frame[frame['room']==roomend[0]]
    if livingend[0]!='选项':
        if livingend[0]=='3':
            frame=frame[frame['living']>'2']
        else:
            frame=frame[frame['living']==livingend[0]]
    if bathend[0]!='选项':
        if bathend[0]=='3':
            frame=frame[frame['bath']>'2']
        else:
            frame=frame[frame['bath']==bathend[0]]
    if directionend[0]!='选项':
        frame=frame[frame['direction']==directionend[0]]
    if houseend[0]!='选项':
        frame=frame[frame['house']==houseend[0]]
    frame['height'] = frame['height'].astype(float)
    if heightend[0]!='选项':
        if heightend[0]=='0':
            frame=frame[frame['height']>=1]
            frame=frame[frame['height']<=20]
        elif heightend[0]=='1':
            frame = frame[frame['height'] >= 20]
            frame = frame[frame['height'] <= 60]
        elif heightend[0]=='2':
            frame = frame[frame['height'] >= 40]
            frame = frame[frame['height'] <= 60]
        else:
            frame=frame[frame['height']>=60]
    if decorationend[0]!='选项':
        frame=frame[frame['decoration']==decorationend[0]]
    frame['area'] = frame['area'].astype(float)
    frame['avgprice'] = frame['avgprice'].astype(float)
    frame['total'] = frame['total'].astype(float)
    if len(areaminend[0])!=0:
        frame=frame[frame['area']>float(areaminend[0])]
    if len(areamaxend[0])!=0:
        frame=frame[frame['area']<float(areamaxend[0])]
    if len(avgminend[0])!=0:
        frame=frame[frame['avgprice']>float(avgminend[0])]
    if len(avgmaxend[0])!=0:
        frame = frame[frame['avgprice'] < float(avgmaxend[0])]
    if len(totalminend[0])!=0:
        frame=frame[frame['total']>float(totalminend[0])]
    if len(totalmaxend[0])!=0:
        frame = frame[frame['total'] < float(totalmaxend[0])]
    newdata={"name": [i for i in frame['name']],
            "region":[i for i in frame['region']],
            "place": [i for i in frame['place']],
            "room": [i for i in frame['room']],
            "living":[i for i in frame['living']],
            "kitchen":[i for i in frame['kitchen']],
            "bath": [i for i in frame['bath']],
            "area": [i for i in frame['area']],
            "avgprice":[i for i in frame['avgprice']],
            "total": [i for i in frame['total']],
            "direction": [i for i in frame['direction']],
            "house": [i for i in frame['house']],
            "height":[i for i in frame['height']],
            "decoration":[i for i in frame['decoration']],
            "href":[i for i in frame['href']],
            }
    return JsonResponse(newdata)


def getrenthouse(request):
    location = request.GET.get('currentlocation')
    Location = re.sub(u"\\(.*?\\)", "", location)
    renthousesql = "select * from renthousedispose where 小区名称 like '%%%%%s%%%%'" % Location
    rentdata = get_data(renthousesql)
    jsondata = {"name": [i[0] for i in rentdata],
                "region": [i[1] for i in rentdata],
                "place": [i[2] for i in rentdata],
                "room": [i[3] for i in rentdata],
                "living": [i[4] for i in rentdata],
                "bath": [i[5] for i in rentdata],
                "area": [i[6] for i in rentdata],
                "rentprice": [i[7] for i in rentdata],
                "direction": [i[8] for i in rentdata],
                "house": [i[9] for i in rentdata],
                "height": [i[10] for i in rentdata],
                "href": [i[11] for i in rentdata],
                }
    return JsonResponse(jsondata)
def getsechouse(request):
    location = request.GET.get('currentlocation')
    Location = re.sub(u"\\(.*?\\)", "", location)
    sechousesql = "select * from sechousedisposed where 小区名称 like '%%%%%s%%%%'" % Location
    secdata = get_data(sechousesql)
    jsondata = {"name": [i[0] for i in secdata],
                "region": [i[1] for i in secdata],
                "place": [i[2] for i in secdata],
                "room": [i[3] for i in secdata],
                "living": [i[4] for i in secdata],
                "kitchen": [i[5] for i in secdata],
                "bath": [i[6] for i in secdata],
                "area": [i[7] for i in secdata],
                "avgprice": [i[8] for i in secdata],
                "total": [i[9] for i in secdata],
                "direction": [i[10] for i in secdata],
                "house": [i[11] for i in secdata],
                "height": [i[12] for i in secdata],
                "decoration": [i[13] for i in secdata],
                "href": [i[14] for i in secdata],
                }
    return JsonResponse(jsondata)