from aliyunsdkcore import client
from aliyunsdkr_kvstore.request.v20150101.DescribeHistoryMonitorValuesRequest import DescribeHistoryMonitorValuesRequest
import sys
import json
import requests
import datetime
from time import time

# 阿里云密钥
ID = ''
Secret = ''
# RegionID = 'cn-shenzhen'  实例地区
RegionID = sys.argv[1]
Step = 60
# DBInstanceID = ""         实例ID
DBInstanceID = sys.argv[2]
MasterKey = "MemoryUsage,UsedQPS,QPSUsage,Hit_Rate_Monitor,CpuUsage"


# 新建AcsClient
client = client.AcsClient(ID, Secret, RegionID)
url = "http://www.iots.vip:2080/v1/push"


def GetRedisPerformance(DBInstanceID, MasterKey):
    '''
    阿里云返回的数据为 UTC 时间，因此要转换为东八区时间。其他时区同理。
    最小时间间隔为 1 分钟，因此这里选择时间跨度为 1 分钟
    '''
    UTC_End = datetime.datetime.today() - datetime.timedelta(hours=8)
    UTC_Start = UTC_End - datetime.timedelta(minutes=1)
    StartTime = datetime.datetime.strftime(UTC_Start, '%Y-%m-%dT%H:%M:%SZ')
    EndTime = datetime.datetime.strftime(UTC_End, '%Y-%m-%dT%H:%M:%SZ')
    Performance = DescribeHistoryMonitorValuesRequest()
    Performance.set_accept_format('json')
    Performance.set_InstanceId(DBInstanceID)
    Performance.set_MonitorKeys(MasterKey)
    Performance.set_IntervalForHistory("01m")
    Performance.set_StartTime(StartTime)
    Performance.set_EndTime(EndTime)
    PerformanceInfo = client.do_action_with_exception(Performance)
    Info = json.loads(PerformanceInfo)
    a = json.loads(Info['MonitorHistory'])
    MetricToValue = dict()
    for i in a:
        MetricToValue = a[i]
        break
    return MetricToValue


'''
MetricToValue 传入metric-value字典  
'''
def PushToN9e(Endpoint, RegionID, MetricToValue, Step):
    data = list()
    for i in MetricToValue:
        tmp = [
            {
                "endpoint": Endpoint,
                "metric": i,
                "tagsMap": {
                    "Region": RegionID
                },
                "value": float(MetricToValue[i]),
                "timestamp": int(time()),
                "step": int(Step)
            }
        ]
        data.extend(tmp)

    res = requests.post(url, json=data)
    if '{"err":""}' == res.text:
        print("success")
    else:
        print(res.text)
        exit(1)


def main():
    PushToN9e("redis-" + DBInstanceID, RegionID, GetRedisPerformance(DBInstanceID, MasterKey), Step)


if __name__ == '__main__':
    main()

