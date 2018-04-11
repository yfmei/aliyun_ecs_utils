# -*- coding:utf-8 -*-
# Created by yfmei on 2018/4/5.
from aliyunsdkecs.request.v20140526 import AllocatePublicIpAddressRequest
from ecs_config import *
import json


def allocate_public_address(instance_id):
    """
    为实例申请公网ip, 异常如下
    1、只有运行中和已停止可以申请
    2、当VPC类型实例已经绑定了 EIP，则无法再分配公网 IP。
    3、一台实例只能分配一个公网 IP 地址。如果实例已经拥有一个公网 IP 地址，将报错 AllocatedAlready。
    4、重启实例（RebootInstance）或者启动实例（StartInstance）后，新的公网 IP 地址生效。
    5、被 安全控制 的实例的 OperationLocks 中标记了 "LockReason" : "security" 时，不能分配公网 IP 地址。
    :return:
    """
    request = AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
    request.set_InstanceId(instance_id)
    # 发起请求, 返回json = { RequestId,InstanceId }
    response = client.do_action_with_exception(request)
    IpAddress = json.loads(response)["IpAddress"]
    print("为实例申请公网ip: {}".format(IpAddress))
    return response


if __name__ == '__main__':

    # 加载instance_id
    instance_id = 0
    with open(file_name, "r") as f:
        for line in f:
            instance_id = line.strip()

    allocate_public_address(instance_id)  # 异常
