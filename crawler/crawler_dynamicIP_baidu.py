#!/usr/bin/env python
#coding=utf-8

from urllib import request
from urllib import parse
import urllib
import io
import re
import sys
import time
import datetime
def getIP():
    #The url_ip is the address which you get proxy
    url_ip = 'http://www.mogumiao.com/proxy/api/get_ip_bs?appKey=4f480e45baeb4e4099c3944136854ef0&count=1&expiryDate=0&format=2'
    req = urllib.request.Request(url_ip)
    data = urllib.request.urlopen(req).read()
    print(data.decode())
    return data.decode().replace('\n','')
#refresh_time is the second number in clock you want to refresh the ip
def crawler_baidu(vocabulary_address,save_address):
    agent_list = []
    vocabulary_list = []
    vocabulary_dict = {}
    vocabulary_dict2 = {}

    #The content which you want to get by crawler
    vocabulary_open = open(vocabulary_address,'r',encoding='utf-8')
    vocabulary_read = vocabulary_open.readlines()
    for line in vocabulary_read:
        line = line.replace('\r','')
        line = line.replace('\n','')
        temp = line.split('\t')
        vocabulary_dict[temp[0]] = temp[1]
        vocabulary_dict2 = {temp[0] : temp[1]}
        vocabulary_list.append(vocabulary_dict2)
    vocabulary_open.close()
    save_open = open(save_address,'a',encoding='utf-8')
    proxy = {'https': getIP()}
    now = datetime.datetime.now()
    now.strftime('%Y-%m-%d %H:%M:%S')
    old = now
    temp = 0
    for translate in vocabulary_list:
        key = ''
        print(proxy)
        now = datetime.datetime.now()
        now.strftime('%Y-%m-%d %H:%M:%S')
        print(now)
        if (now.minute - old.minute>2) and temp >= 10:
            ip = getIP()
            if 'code' in ip:
                temp = 0
            else:
                proxy = {'https': ip}
                old = now
        for k in translate:
            key = k
        search_content = key + '+' + parse.quote(translate[key])
        url = 'http://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&rsv_idx=1&tn=baidu&wd=' + search_content
        num = ''
        try:
            proxy_support = request.ProxyHandler(proxy)
            opener = request.build_opener(proxy_support)
            opener.addheaders = [('User-Agent','Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19')]
            request.install_opener(opener)
            response = request.urlopen(url)
            html = response.read().decode("utf-8")
            num = html.split('百度为您找到相关结果约')
            if len(num) >= 2:
                num = num[1].split('个')
                num = num[0].replace(',','')
            else:
                num = 'error'
        except:
            num = 'error'
        save_content = key + '\t' + translate[key] + '\t' + num + '\n'
        save_open.writelines(save_content)
        temp = temp + 1
    save_open.close()
crawler_baidu('/home/py35/crawler_dynamicIP_baidu_vocabulary.txt','/home/py35/save.txt')
