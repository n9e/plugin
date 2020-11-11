#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import time
import commands

'''根据pm2 list 查看 restart 值，累加不等于 0 则为 app 发生过重启'''

items = []


def get_restart_num():
    item = dict()
    item["metric"] = "pm2.restart.status"
    item["tagsMap"] = {
        "srv": "",
        "project": ""
    }
    
    '''根据自己的 app 名来修改 '''
    cmd = "pm2 list | grep -E 'User|emit|timing|app1' | awk '{sum+=$16}END{print sum}'"

    (status, output) = commands.getstatusoutput(cmd)
    if status == 0:
        restart_num = int(output)
        item["value"] = restart_num
        items.append(item)


def main():
    timestamp = int(time.time())
    get_restart_num()

    for item in items:
        item["timestamp"] = timestamp

    print(json.dumps(items))


if __name__ == '__main__':
    main()
