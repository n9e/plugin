#!/usr/bin/python
#coding=utf8
import time
import json
import copy
import commands

ts = int(time.time())
payload = []
data = {"endpoint":"","metric":"","timestamp":ts,"value":0,"counterType":"GAUGE","tags":""}

a,pdns_stat = commands.getstatusoutput('rec_control get cache-hits')
q_hit_first = pdns_stat.split("\n")[0]

a,pdns_stat = commands.getstatusoutput('rec_control get cache-misses')
q_miss_first = pdns_stat.split("\n")[0]

a,pdns_stat = commands.getstatusoutput('rec_control get packetcache-hits')
pkt_hit_first = pdns_stat.split("\n")[0]
a,pdns_stat = commands.getstatusoutput('rec_control get packetcache-misses')
pkt_miss_first = pdns_stat.split("\n")[0]
time.sleep(5)

a,pdns_stat = commands.getstatusoutput('rec_control get cache-hits')
q_hit_last = pdns_stat.split("\n")[0]

a,pdns_stat = commands.getstatusoutput('rec_control get cache-misses')
q_miss_last = pdns_stat.split("\n")[0]

a,pdns_stat = commands.getstatusoutput('rec_control get packetcache-hits')
pkt_hit_last = pdns_stat.split("\n")[0]

a,pdns_stat = commands.getstatusoutput('rec_control get packetcache-misses')
pkt_miss_last = pdns_stat.split("\n")[0]

pkt_hit = float(pkt_hit_last) - float(pkt_hit_first)
pkt_miss = float(pkt_miss_last) - float(pkt_miss_first)
q_hit = float(q_hit_last) - float(q_hit_first)
q_miss = float(q_miss_last) - float(q_miss_first)

hit_rate = 0

if (pkt_hit + q_hit) != 0:
    hit_rate = 100 * (pkt_hit + q_hit)/(pkt_hit + pkt_miss + q_hit + q_miss)

data["metric"] = "pdns-recursor.hit_rate"
data["value"] = hit_rate

payload.append(copy.copy(data))
print json.dumps(payload,indent=4)
