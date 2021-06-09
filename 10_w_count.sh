#!/bin/bash

Activities=$(w |awk -F ':' '{if(NR>2) print $1}' |wc -l)

localip=$(/usr/sbin/ifconfig `/usr/sbin/route|grep '^default'|awk '{print $NF}'`|grep inet|awk '{print $2}'|head -n 1)
step=$(basename $0|awk -F'_' '{print $1}')
timestamp=$(date +%s)
echo '[
    {
        "endpoint": "'${localip}'",
        "tags": "",
        "timestamp": '${timestamp}',
        "metric": "sys.w.count",
        "value": '${Activities}',
        "step": '${step}'
    }
]'
