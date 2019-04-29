import json
str = "  Lihua is good man!     "
str1='{"name":"Lihua","ages":18,"weigth":140,"heigth":170}'
#非字典类型的字符串，会报错！
dic1 = json.dumps(str)
print(dic1)
print(type(dic1))
dic2=json.loads(str1)
print(dic2)