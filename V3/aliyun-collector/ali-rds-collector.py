from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeDBInstancePerformanceRequest
import sys
import json
import requests
import datetime
from time import time

# 阿里云密钥
ID = ''
Secret = ''

Step = 60
# RegionID = ''
RegionID = sys.argv[1]
# DBInstanceID = ""
DBInstanceID = sys.argv[2]
MasterKey = "MySQL_NetworkTraffic,MySQL_QPSTPS,MySQL_Sessions,MySQL_InnoDBBufferRatio,MySQL_InnoDBDataReadWriten,MySQL_InnoDBLogRequests,MySQL_InnoDBLogWrites,MySQL_TempDiskTableCreates,MySQL_MyISAMKeyBufferRatio,MySQL_MyISAMKeyReadWrites,MySQL_COMDML,MySQL_RowDML,MySQL_MemCpuUsage,MySQL_IOPS,MySQL_DetailedSpaceUsage,MySQL_CPS,slavestat,MySQL_ThreadStatus,MySQL_ReplicationDelay,MySQL_ReplicationThread"
# 域名替换为n9e的
url = "http://www.iots.vip:2080/v1/push"
# 新建AcsClient
client = client.AcsClient(ID, Secret, RegionID)


'''
获取性能指标
DBInstanceId  实例ID
MasterKey     性能指标键值  来自https://help.aliyun.com/document_detail/26316.html?spm=a2c4g.11186623.2.10.7e342389yXFV1d
return type dict
'''


def GetPerformance(DBInstanceID, MasterKey):
    '''
    阿里云返回的数据为 UTC 时间，因此要转换为东八区时间。其他时区同理。
    最小时间间隔为 1 分钟，因此这里选择时间跨度为 1 分钟
    '''
    UTC_End = datetime.datetime.today() - datetime.timedelta(hours=8)
    UTC_Start = UTC_End - datetime.timedelta(minutes=1)
    StartTime = datetime.datetime.strftime(UTC_Start, '%Y-%m-%dT%H:%MZ')
    EndTime = datetime.datetime.strftime(UTC_End, '%Y-%m-%dT%H:%MZ')
    Performance = DescribeDBInstancePerformanceRequest.DescribeDBInstancePerformanceRequest()
    Performance.set_accept_format('json')
    Performance.set_DBInstanceId(DBInstanceID)
    Performance.set_Key(MasterKey)
    Performance.set_StartTime(StartTime)
    Performance.set_EndTime(EndTime)
    PerformanceInfo = client.do_action_with_exception(Performance)
    Info = json.loads(PerformanceInfo)
    Value = Info['PerformanceKeys']['PerformanceKey']
    MetricToValue = dict()
    for i in Value:
        a = dict()
        if "&" in str(i):
            vf = i["ValueFormat"].split('&')
            vl = i["Values"]["PerformanceValue"][0]["Value"].split('&')
            l = len(vf)
            while l != 0:
                l -= 1
                a[vf[l]] = vl[l]
        else:
            a[i['ValueFormat']] = i['Values']['PerformanceValue'][0]['Value']
        MetricToValue.update(a)
    return MetricToValue


'''
推送至n9e
MetricTovalue 为 metric-value 字典
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
    MetricToValue = GetPerformance(DBInstanceID, MasterKey)
    PushToN9e("rds-" + DBInstanceID, RegionID, MetricToValue, Step)


if __name__ == '__main__':
    main()

