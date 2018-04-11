# -*- coding:utf-8 -*-
# Created by yfmei on 2018/4/4.
# 导入相关sdk
from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
from ecs_config import *
import json
from desc_instance import desc_instance_status, desc_instance_info
from allocate_public_address import allocate_public_address
from start_instance import start


def create():
    """

    :return: InstanceId
    """
    # 创建新实例
    request = CreateInstanceRequest.CreateInstanceRequest()
    request.set_ImageId("m-hp30yonwqwwz5tqwlhaq")  # 镜像ID
    request.set_InstanceName("aliyun")  # 设置实例名称, 显示在控制台
    request.set_InstanceType("ecs.gn5-c8g1.2xlarge")  # 实例资源规格: tesla p100, 内存: 60G, 硬盘(2个): 40G, 400G 2.6一小时
    request.set_SecurityGroupId("sg-hp3f3jpmruir2y5qtscs")  # 安全组ID, 比默认多开了8888
    # 实例规格族 https://www.alibabacloud.com/help/zh/doc-detail/25378.htm?spm=a3c0i.o25620zh.a3.1.2a2915d8lmwOC0
    # ================== 网络 ==================
    # 参数	    InternetChargeType	InternetMaxBandwidthOut
    #           PayByBandwidth	    按固定带宽付费。
    # 参数取值                      为所选的固定带宽值。
    #           PayByTraffic	    按使用流量付费。
    #                               带宽的上限设置，计费以实际使用的网络流量为依据。
    request.set_InternetChargeType("PayByTraffic")  # 网络计费类型, 按使用流量配置, PayByTraffic为默认值
    # todo 申请公网ip必须要设置大于0的值, 默认值为0
    # 公网出带宽最大值, 单位 Mbit/s, 范围: 按带宽计费：[0, 100]; 按流量计费：[0, 100]
    request.set_InternetMaxBandwidthOut("5")  # InternetMaxBandwidthIn 的值在任何情况下都与计费无关，实例的入数据流量是免费的。
    # ================== 网络 ==================
    request.set_HostName("aliyun")  # 服务器主机名
    request.set_SystemDiskCategory("cloud_efficiency")  # 系统盘类型: 高效云盘
    request.set_SystemDiskSize("40")  # 系统盘大小, 默认值: max{40, ImageSize}
    # PrePaid：预付费，即包年包月。选择该类付费方式的用户必须确认自己的账号支持余额支付/信用支付，否则将返回 InvalidPayMethod 的错误提示。
    # PostPaid：后付费，即按量付费。
    request.set_InstanceChargeType("PostPaid")  # 实例付费类型, 默认值：PostPaid 后付费
    # NoSpot：正常按量付费实例
    # SpotWithPriceLimit：设置上限价格的竞价实例
    # SpotAsPriceGo：系统自动出价，最高按量付费价格。
    request.set_SpotStrategy("NoSpot")  # 后付费的竞价策略, 当参数 InstanceChargeType 取值为 PostPaid 时为生效, 默认值：NoSpot

    # 通过提供ClientToken参数保证请求的幂等性。ClientToken是一个由客户端生成的唯一的、大小写敏感、不超过64个ASCII字符的字符串。
    # 1、如果用户使用同一个ClientToken值调用创建实例接口，则服务端会返回相同的请求结果，包含相同的InstanceId。
    # 因此用户在遇到错误进行重试的时候，可以通过提供相同的ClientToken值，来确保ECS只创建一个实例，并得到这个实例的InstanceId。
    # 2、如果用户提供了一个已经使用过的ClientToken，但其他请求参数不同，则ECS会返回IdempotentParameterMismatch的错误代码。
    # 但需要注意的是，SignatureNonce、Timestamp和Signature参数在重试时是需要变化的，因为ECS使用SignatureNonce来防止重放攻击，使用Timestamp来标记每次请求时间，所以再次请求必须提供不同的SignatureNonce和Timestamp参数值，这同时也会导致Signature值的变化。
    # 3、通常，客户端只需要在500（InternalErrorInternalError）或503（ServiceUnavailable）错误、或者无法得到响应结果的情况下进行重试操作。
    # 返回结果是200时，重试可以得到上次相同的结果，但不会对服务端状态带来任何影响。而对4xx的返回错误，除非提示信息里明确出现“try it later”，通常重试也是不能成功的。
    timestamp = time.time()
    # 防止请求超时或服务器内部错误时，等原因, 客户端重试请求, 创建比预期要多的实例
    request.set_ClientToken("skskskskskkffffffg" + str(timestamp))

    # 发起请求, 返回json = { RequestId,InstanceId }
    response = client.do_action_with_exception(request)
    print("创建实例: {}".format(response))
    # 创建的实例id
    instance_id = json.loads(response).get("InstanceId")

    # 保存instance_id, 启动后追加公网ip等信息
    with open(file_name, "w") as f:
        f.write(instance_id)
    # save(instance_id)  # todo 此时应该获取不到公网ip
    while True:
        # 检测实例状态, 可能实例还没创建好
        instance_status = desc_instance_status([instance_id])
        if instance_status == "Stopped":  # 刚开始是 Pending, 初始化后为Stopped
            print("实例已创建, 申请公网ip...")
            # 为实例申请公网ip
            allocate_public_address(instance_id)
            print("公网ip已申请, 启动实例...")
            # 启动实例
            start(instance_id)
            # 追加公网ip等信息
            # save(instance_id, title=title, filename=file_name)
        elif instance_status == "Running":
            # 保存日志, 运行中才看到公网ip
            save(instance_id)
            break

    return instance_id


def save(instance_id, title=title, filename=log_filename):
    """
    保存日志文件, 不存在就创建并写入title, 存在就添加
    :param data: 保存内容, type: 二维数组, 每行代表一条数据
    :param instance_id: 实例id
    :param title: 标题, type: list
    :param log_path: 保存的文件名
    :return:
    """

    test = False
    if test:
        with open("instance_info_sample.txt", "r") as f:
            instance_info = " ".join(f.readlines()).strip("\n")
        instance_info = json.loads(instance_info)
    else:
        instance_info = desc_instance_info([instance_id])

    instance = instance_info["Instances"]["Instance"][0]

    content = construct_content(instance, title)

    if not os.path.exists(filename):
        # 存在就覆盖, 不存在新建并写入title
        with open(filename, "w") as f:
            f.write(" ".join(title))
    # 追加内容
    with open(filename, "a") as f:
        f.write("\n" + content)


def construct_content(instance, title):
    print(instance)

    lst = [str(instance[i]) if i != "PublicIpAddress" else instance[i]["IpAddress"][0] for i in title]
    content = " ".join(lst)
    print(content)
    # content += instance["CreationTime"]
    # content += "," + instance["InstanceId"]
    # content += "," + instance["HostName"]
    # content += "," + instance["InstanceType"]
    # content += "," + instance["InstanceChargeType"]
    # content += "," + instance["PublicIpAddress"]["IpAddress"][0]
    # content += "," + instance["Status"]
    # content += "," + instance["ImageId"]
    # content += "," + instance["IoOptimized"]
    # content += "," + instance["RegionId"]
    return content


if __name__ == '__main__':

    create()

