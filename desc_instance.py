# -*- coding:utf-8 -*-
# Created by yfmei on 2018/4/5.
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest, DescribeInstanceTypesRequest
from ecs_config import *
import json


def desc_instance_types():
    """
    查询云服务器 ECS 提供的实例规格资源
    :return:
    """
    request = DescribeInstanceTypesRequest.DescribeInstanceTypesRequest()
    return request


def desc_instance_status(instance_ids):
    """
    检测实例状态
    Running
    Starting
    Stopping
    Stopped
    :param instance_ids:
    :return:
    """
    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_InstanceIds(instance_ids)
    response = client.do_action_with_exception(request)
    result = json.loads(response)
    # print(result.keys())
    # print(result)
    status = result["Instances"]["Instance"][0]["Status"]
    desc = ""
    if status == "Running":
        desc = "实例运行中... 实例状态: %s"
    elif status == "Starting":
        desc = "实例启动中... 实例状态: %s"
    elif status == "Stopping":
        desc = "实例停止中... 实例状态: %s"
    elif status == "Stopped":
        desc = "实例已停止... 实例状态: %s"
    elif status == "Pending":
        desc = "实例初始化中... 实例状态: %s"
    print(desc % status)
    return status


def desc_instance_info(instance_ids):
    """
    检测实例详情
    :param instance_ids:
    :return: json
    """
    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_InstanceIds(instance_ids)
    response = client.do_action_with_exception(request)
    result = json.loads(response)
    # print(result.keys())
    # print(result)

    return result
