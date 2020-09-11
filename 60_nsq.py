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


url = 'http://127.0.0.1:4171/api/topics'
username = ''
password = ''

def get_topic_info():
    req = urllib2.HTTPPasswordMgrWithDefaultRealm()
    handler = urllib2.HTTPBasicAuthHandler(req)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    page = urllib2.urlopen(url,timeout=3)
    html = page.read()
    topics = json.loads(html)['topics']
#   topics_len = len(topics)
#   print(topics)
    return(topics)

def get_queues_info(url1):
    url_all = url + "/" + url1
    req = urllib2.HTTPPasswordMgrWithDefaultRealm()
    handler = urllib2.HTTPBasicAuthHandler(req)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    page = urllib2.urlopen(url_all,timeout=3)
    html = page.read()
    html_json = json.loads(html)
    try:
       depth_resoult = html_json['channels'][0]['depth']
       if depth_resoult:
          depth_resoult = depth_resoult
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

def output_resoult(url1):
    output = []
    t = {}
    key_word = 'channel_name'
    t['endpoint'] = get_ip_address('endpoint')
    t['metric'] = 'nsq.%s' % url1
    t['tags'] = ''
    t['timestamp'] = int(time.time())
    t['step'] = 60
    t['value'] = get_queues_info(url1)
    t['counterType'] = 'GAUGE'
    output.append(t)
    return output

if __name__ == "__main__":
    ts = get_topic_info()
    m_output = []
    for t in ts:
        d = output_resoult(t)
        if d:
        #使用extend进行多数组合并
            m_output.extend(d)
    print(json.dumps(m_output))
#            print(json.dumps(m_output))
    #        requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(m_output),timeout=50)


