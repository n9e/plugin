# pdns-recursor 采集脚本

## 系统需求

Linux 
Python >= 2.6

## 使用

先手动执行脚本，观察运行状态。如无异常，在 n9e 内配置对应目录采集即可

## 指标
所有指标的前缀均为 `pdns-recursor.`，可以以此为关键字在 n9e 中搜索。

`pdns-monitor.py` 采集所有 `rec_control get-all` 返回的监控指标，详细的指标说明可以参考 [官方文档](https://doc.powerdns.com/recursor/metrics.html#using-rec-control)

`pdns-cache-hit.py` 统计 dns 的缓存命中率，根据 `(cache-hits + packetcache-hits)/(cache-hits + packetcache-hits + cache-misses + packetcache-misses)` 计算

上报的指标为 `pdns-recursor.hit_rate`
