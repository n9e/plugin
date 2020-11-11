#!/usr/bin/python
#coding=utf8
import time
import json
import copy
import commands

ts = int(time.time())
payload = []
data = {"endpoint":"","metric":"","timestamp":ts,"step":60,"value":"","counterType":"GAUGE","tags":""}

a,pdns_stat = commands.getstatusoutput('pdns_control show query-cache-hit')
q_hit_first = pdns_stat.split("\n")[0]

a,pdns_stat = commands.getstatusoutput('pdns_control show query-cache-miss')
q_miss_first = pdns_stat.split("\n")[0]

a,pdns_stat = commands.getstatusoutput('pdns_control show packetcache-hit')
pkt_hit_first = pdns_stat.split("\n")[0]
a,pdns_stat = commands.getstatusoutput('pdns_control show packetcache-miss')
pkt_miss_first = pdns_stat.split("\n")[0]
time.sleep(5)

a,pdns_stat = commands.getstatusoutput('pdns_control show query-cache-hit')
q_hit_last = pdns_stat.split("\n")[0]

a,pdns_stat = commands.getstatusoutput('pdns_control show query-cache-miss')
q_miss_last = pdns_stat.split("\n")[0]

a,pdns_stat = commands.getstatusoutput('pdns_control show packetcache-hit')
pkt_hit_last = pdns_stat.split("\n")[0]

a,pdns_stat = commands.getstatusoutput('pdns_control show packetcache-miss')
pkt_miss_last = pdns_stat.split("\n")[0]

pkt_hit = float(pkt_hit_last) - float(pkt_hit_first)
pkt_miss = float(pkt_miss_last) - float(pkt_miss_first)
q_hit = float(q_hit_last) - float(q_hit_first)
q_miss = float(q_miss_last) - float(q_miss_first)

hit_rate = 0

if (pkt_hit + q_hit) != 0:
    hit_rate = 100 * (pkt_hit + q_hit)/(pkt_hit + pkt_miss + q_hit + q_miss)

data["metric"] = "pdns.hit_rate"
data["value"] = hit_rate

payload.append(copy.copy(data))
print json.dumps(payload,indent=4)
