# -*- coding:utf-8 -*- 

import time

def timeform(dt1):
    msgtime = str(dt1)
    mili = str(msgtime)[-6:]
    msgtime = str(msgtime)[:-7]
    msgtime = time.strptime(msgtime,'%Y-%m-%d %H:%M:%S')
    msgtime = time.mktime(msgtime)
    msgtime = float(str(msgtime)[:-1] + mili)
    return msgtime