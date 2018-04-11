# -*- coding:utf-8 -*-
# Created by yfmei on 2018/4/5.
from aliyunsdkecs.request.v20140526 import StopInstanceRequest
from aliyunsdkecs.request.v20140526 import DeleteInstanceRequest
from desc_instance import desc_instance_status
from ecs_config import *


def stop(instance_id):
    request = StopInstanceRequest.StopInstanceRequest()
    request.set_InstanceId(instance_id)
    response = client.do_action_with_exception(request)
    print("停止实例: {}".format(response))


def delete(instance_id):
    request = DeleteInstanceRequest.DeleteInstanceRequest()
    request.set_InstanceId(instance_id)
    response = client.do_action_with_exception(request)
    print("释放实例: {}".format(response))


if __name__ == '__main__':

    # 加载instance_id
    instance_id = 0
    with open(file_name, "r") as f:
        for line in f:
            instance_id = line.strip()

    while True:

        instance_status = desc_instance_status([instance_id])
        if instance_status == "Running":
            stop(instance_id)
        elif instance_status == "Stopped":
            delete(instance_id)
            break
