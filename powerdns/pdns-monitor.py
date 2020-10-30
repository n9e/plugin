#!/usr/bin/python
#coding=utf8
import time
import json
import copy
import commands


ts = int(time.time())
payload = []
data = {"endpoint":"","metric":"","timestamp":ts,"value":0,"counterType":"COUNTER","tags":""}

gauge_metrics = [
"tcp-clients",
"fd-usage",
"throttle-entries",
"nsspeeds-entries",
"cache-entries",
"concurrent-queries",
"max-mthread-stack",
"packetcache-entries",
"negcache-entries",
"qa-latency",
"uptime",
"x-our-latency",
"failed-host-entries",
]

a,pdns_stat = commands.getstatusoutput('rec_control get-all')
pdns_array = pdns_stat.split("\n")
for stat in pdns_array:
	pdns = stat.split("\t")
	metric = pdns[0]
	value = pdns[1]
	data["metric"] = "pdns-recursor." + metric
	data["value"] = int(value)
	if metric in gauge_metrics:
            data["counterType"] = "GAUGE"
	else:
            data["counterType"] = "COUNTER"
	payload.append(copy.copy(data))

print json.dumps(payload,indent=4)
