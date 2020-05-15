#!/usr/bin/env python
# -*- coding: utf-8 -*-
#一个积压，正常20000的阈值
from xml.etree import ElementTree as ET
from itertools import chain
import time
import json
import socket
import urllib2
import requests
import commands

url = 'http://127.0.0.1:4171/api/topics/Envision'
username = ''
password = ''

def get_queues_info():
    req = urllib2.HTTPPasswordMgrWithDefaultRealm()
    handler = urllib2.HTTPBasicAuthHandler(req)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    page = urllib2.urlopen(url,timeout=3)
    html = page.read()
    html_json = json.loads(html)
    try:
       depth_resoult = html_json['channels'][0]['depth']
       if depth_resoult:
          print(depth_resoult)
    except:   
       depth_resoult = 0
    return depth_resoult

def get_ip_address(key):
    if key=='ip':
        return socket.gethostbyname(socket.gethostname())
    elif key=='hostname':
        return socket.gethostname()
    elif key=='endpoint':
        endpoint = commands.getoutput('''ifconfig `route|grep '^default'|awk '{print $NF}'`|grep inet|awk '{print $2}'|awk -F ':' '{print $NF}'|head -n 1 ''')
        return endpoint

def output_resoult():
    output = []
    t = {}
    key_word = 'Edge_DataCollection'
    t['endpoint'] = get_ip_address('endpoint')
    t['timestamp'] = int(time.time())
    t['step'] = 60
    t['tags'] = 'name=nsq'
    t['metric'] = 'nsq_%s' % key_word
    t['value'] = get_queues_info()
    t['counterType'] = 'GAUGE'
    output.append(t)
    return output

if __name__ == "__main__":
    d = output_resoult()
    if d:
        print(json.dumps(d))
#        requests.post("http://127.0.0.1:2058/api/collector/push", data=json.dumps(d),timeout=50)
