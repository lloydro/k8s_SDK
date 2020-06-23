import time
import hashlib
import random
import math
import uuid
import re


def datetime_now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def md5(data):
    m = hashlib.md5()
    b = data.encode(encoding='utf-8')
    m.update(b)
    return m.hexdigest()

# K/M/G unit transform
def nomalize_unit(data):
    backup = data
    reExp = re.compile(r'\d+')
    data = re.findall(reExp, data)
    if len(data) > 0:
        data = data[0]
    else:
        data = "0"
    if  backup.find('G') != -1:
        data = int(data) * 1024 * 1024 * 1024
    elif  backup.find('M') != -1:
        data = int(data) * 1024 * 1024
    elif  backup.find('K') != -1:
        data = int(data) * 1024
    elif  backup.find('m') != -1:         
        data = int(data) / 1000
    else:
        data = int(data)
    return data

# return random number between 0 - max_data
def random_int(max_data):
    data = max_data*random.random()
    return math.floor(data)

# return random number with 12bit calculated by uuid and timestamp 
def random_uuid_time():
    uuid_number = str(uuid.uuid1()).upper().replace('-','')
    order_number = lambda : int(round(time.time()* 1000))
    time_number = str(order_number())
    return uuid_number[0:6] + time_number[-6:]

# return namespace of a uid 
def get_namespace(uid):     # 账号只能带数字字母下划线，只要处理下划线即可
    uid = uid.replace("_", "-")
    return uid + '-ns'