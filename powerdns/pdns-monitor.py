#!/usr/bin/python
#coding=utf8
import time
import json
import copy
import commands


ts = int(time.time())
payload = []
data = {"endpoint":"","metric":"","timestamp":ts,"step":60,"value":0,"counterType":"COUNTER","tags":""}

gauge_metrics = [
"fd-usage",
"key-cache-size",
"latency",
"meta-cache-size",
"packetcache-size",
"query-cache-size",
"qsize-q",
"real-memory-usage",
"recursing-answers",
"recursing-questions",
"recursion-unanswered",
"security-status",
"signature-cache-size",
"signatures",
"uptime"
]

a,pdns_stat = commands.getstatusoutput('pdns_control list')
pdns_array = pdns_stat.split(",")
for stat in pdns_array:
	if stat == "":
		continue
        pdns = stat.split("=")
        metric = pdns[0]
        value = pdns[1]
        data["metric"] = "pdns." + metric
        data["value"] = int(value)
        if metric in gauge_metrics:
            data["counterType"] = "GAUGE"
        else:
            data["counterType"] = "COUNTER"
        payload.append(copy.copy(data))
print json.dumps(payload,indent=4)
