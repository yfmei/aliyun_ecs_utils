# -*- coding:utf-8 -*-
# Created by yfmei on 2018/4/5.
from aliyunsdkecs.request.v20140526 import StartInstanceRequest

from desc_instance import desc_instance_status
from ecs_config import *


def start(instance_id):
    """
    启动实例
    :return:
    """
    request = StartInstanceRequest.StartInstanceRequest()
    request.set_InstanceId(instance_id)

    response = client.do_action_with_exception(request)
    print("启动实例: {}".format(response))


if __name__ == '__main__':

    # 加载instance_id
    instance_id = 0
    with open(file_name, "r") as f:
        for line in f:
            instance_id = line.strip()
    while True:
        instance_status = desc_instance_status([instance_id])
        if instance_status == "Stopped":
            start(instance_id)
        elif instance_status == "Running":
            break
