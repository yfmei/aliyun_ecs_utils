# -*- coding:utf-8 -*-
# Created by yfmei on 2018/4/5.
import time

import os
from aliyunsdkcore.client import AcsClient

# 实例id文件名, 实例释放时读取
file_name = "instance_id.txt"

# 日志文件标题
title = ["CreationTime", "InstanceId", "HostName", "InstanceType", "InstanceChargeType", "PublicIpAddress",
         "Status", "ImageId", "IoOptimized", "RegionId"]

# 日志文件名
log_filename = time.strftime("%Y%m%d", time.localtime()) + ".txt"
log_filename = os.path.join("logs/", log_filename)

# 创建 AcsClient 实例
client = AcsClient(
   "xxxx",
   "xxxx",
   "cn-huhehaote"  # 华北5
   # "cn-shanghai"  # 华东2
   # 区域ID, 详见: https://www.alibabacloud.com/help/zh/doc-detail/40654.htm?spm=a3c0i.o63440zh.a3.11.4bbc722cxWWPJM
)