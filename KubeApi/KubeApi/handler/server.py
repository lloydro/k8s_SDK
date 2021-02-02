
import json
from typing import List
from pprint import pprint
from os import path
import time
import hashlib
import uuid
import random
import math
import re
from KubeApi.config.settings import REQUEST_URL,SERVER_IP_DELAY,SERVER_IP_TIMES,DEVICE_REBOOT_TIMES
import requests



class ServerHandler(object):
    '''
    Openstack server operator.

    ::

        >>> from KubeApi.api import ApiHandler

    '''

    def __init__(
        self,
        uid
        ):
        self.uid = uid

    
    '''
    create an openstack topo . （创建Openstack拓扑 · 通过模板ID）

    ::
    
        >>> Request example:

        templateCfg = {
            "templateId": "5cb88725-2ebf-4342-ab45-6512505739ff",
            "topoName": "tp1.top",
            "topoLifeDays": 30
        }


        >>> Response example:
        {
            "data": {
                "servers": {
                    "d2b96fdb-d793-4946-a613-c67ffa5a9686": {
                        "server_id": "d2b96fdb-d793-4946-a613-c67ffa5a9686",
                        "name": "instance-server-9DA3E3572131",
                        "image_name": "stcv-4.80.2426.qcow2",
                        "flavor_name": "f-cpu2-mem2g-disk40g",
                        "console_host": "0.0.0.0",
                        "console_port": 0,
                        "addr": "",
                        "label": "kvm-TC",
                        "clusterId": 1,
                        "deviceId": "9a84bb8e-76d0-45d9-af55-231244e1118a",
                        "addr": "172.28.181.141",
                        "console_host": "172.28.181.15",
                        "console_port": 10004,
                    },
                },
                "devices": {
                    "9a84bb8e-76d0-45d9-af55-231244e1118a": {
                        "id": "9a84bb8e-76d0-45d9-af55-231244e1118a",
                        "name": "tester1",
                        "exposeIds": [
                            "2b7c689b-8dee-4eba-ae4c-7da96659983b"
                        ],
                        "cm_server_ids": [
                            "d2b96fdb-d793-4946-a613-c67ffa5a9686"
                        ],
                        "addr": "172.28.181.141",
                        "console_host": "172.28.181.15",
                        "console_port": 10004,
                    },
                },
                "clusterId": 1,
                "node_name": "kolla-compute17",
                "topoId": "38b6bb58-e2c8-459b-b990-a82621d5b828"
            }
            'error': '',
            'status': True
        }

    '''
    def create_ops_topo_by_template_id(self,templateCfg):


        result = {
            'datas': {
                'servers': {},
                'devices': {}
            },
            'error': '',
            'status': False
        }


        reqData = templateCfg
        reqData['uid'] = self.uid

        print("request datas:",reqData)
        
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "python-requests/2.9.1",
        }
        url = REQUEST_URL + "/api/ops/CreateTopoByIdV2"
        response = requests.post(url=url, data=json.dumps(reqData), headers=headers, verify=False)
        response = response.content.decode('UTF-8')
        response = json.loads(response)

        print("response ===========================")
        pprint(response)

        data = response.get('data')
        message = response.get('message').get('error')
        status = response.get('status').get('res')

        print("response status",status)

        if not status:
            result['error'] = message
            return result

        # 创建成功，保存数据
        servers = data.get('servers')
        devices = data.get('devices')
        netList = data.get('netList')    
        clusterId = data.get('clusterId')   
        node_name = data.get('node_name')   
        topoId = data.get('topoId')   

        # 异常处理
        if not servers or not devices:
            result['error'] = '创建完成后未获取到设备或节点信息'
            return result
        
        # 收集所有的server_id
        server_id_list = []
        for server_id,server in servers.items():
            server_id_list.append(server_id)

        # 构造cm_id与dev_id的map，以便后续填充设备资料
        cm_dev_map = {}
        for deviceId,device in devices.items():
            cm_server_ids = device.get('cm_server_ids')
            # for cm_server_id in cm_server_ids:
            # TODO. 默认用第一个管理板的IP
            if len(cm_server_ids) > 0 :
                cm_server_id = cm_server_ids[0]
                cm_dev_map[cm_server_id] = deviceId

        # 定时，轮询获取所有servers的addr/console_host/console_port
        url = REQUEST_URL + "/api/ops/getAddr?clusterId=%s&server_id=" % (str(clusterId),)

        for get_ip_count in range(SERVER_IP_TIMES):

            if len(server_id_list) <= 0:
                break
            
            # 若定时器未获取到所有数据，则返回参数要涵盖这些未获取到数据的server_id
            if get_ip_count == SERVER_IP_TIMES - 1:
                result['error'] = '获取板卡IP和console信息异常，以下server_id无法获取到相关信息:' + str(server_id_list)
                # return result
            
            time.sleep(SERVER_IP_DELAY)

            for server_id in server_id_list:
                ipUrl = url + server_id
                response = requests.get(url=ipUrl, headers=headers, verify=False)
                response = response.content.decode('UTF-8')
                response = json.loads(response)

                ipStatus = response.get('status').get('res')
                ipMessage = response.get('message').get('info')
                ipData = response.get('data')

                if not ipStatus:
                    print(server_id,ipMessage)
                    continue

                addr = ipData.get('addr')
                console_host = ipData.get('console_host')
                console_port = ipData.get('console_port')
                
                if not addr or not console_host or not console_port or console_host=='0.0.0.0':
                    print("%s 获取的addr与console信息异常：addr %s, console_host %s, console_port %s " % (server_id, str(addr), str(console_host), str(console_port)))
                    continue
                    
                # 填充实例参数
                server = servers.get(server_id)
                server['addr'] = addr
                server['console_host'] = console_host
                server['console_port'] = console_port

                #若是管理板，填充设备参数
                if cm_dev_map.get(server_id):
                    device_id = cm_dev_map.get(server_id)
                    device = devices.get(device_id)
                    device['addr'] = addr
                    device['console_host'] = console_host
                    device['console_port'] = console_port

                # 已获取到的，从待轮询列表里移除
                server_id_list.remove(server_id)
                if len(server_id_list) <= 0:
                    break
        
        # 构造回调参数
        result['datas']['servers'] = servers
        result['datas']['devices'] = devices
        result['datas']['clusterId'] = clusterId
        result['datas']['node_name'] = node_name
        result['datas']['topoId'] = topoId
        result['datas']['netList'] = netList

        # 最终判断是否有异常
        if not result['error']:
            result['status'] = True

        print("result========================")
        pprint(result)
        return result










    '''
    switch an openstack topo . （切换Openstack拓扑）

    ::
    
        >>> Request example:

        switchCfg = {
            "clusterId": 1,
            "node_name": "kolla-compute17",
            "topoId": "7ea6542b-a717-4630-bbde-90a4491c26a2",
            "topoName": "switchTest", 
            "networkNum": 3,
            "newTopo": {
                "560d837c-11c0-43d2-b70b-6fa2816178e5" : [ 
                    "net1",
                    "net2"
                ]
            },
            "is_reboot_exp": 1
        }


        >>> Response example:
        {
            "status": True,
            "error": "",
            "data": {}
        }

    '''
    def switch_ops_topo(self,switchCfg):


        result = {
            'datas': {},
            'error': '',
            'status': False
        }

        reqData = switchCfg
        reqData['uid'] = self.uid

        print("switch_ops_topo request datas:",reqData)
        
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "python-requests/2.9.1",
        }
        url = REQUEST_URL + "/api/ops/switchTopo"
        response = requests.post(url=url, data=json.dumps(reqData), headers=headers, verify=False)
        response = response.content.decode('UTF-8')
        response = json.loads(response)

        print("response ===========================")
        pprint(response)

        data = response.get('data')
        info = response.get('message').get('info')
        critical_error = response.get('message').get('critical_error')
        status = response.get('status').get('res')

        print("response status",status)

        if not status:
            result['error'] = "error: %s  \r\n  critical_error: %s " % (str(info), str(critical_error) )
            return result

        # 切换成功，重启设备(这里仅重启LC)
        is_reboot_exp = switchCfg.get('is_reboot_exp')
        newTopo = switchCfg.get('newTopo')
        clusterId = switchCfg.get('clusterId')
        if is_reboot_exp:
            for deviceId, linkList in newTopo.items():
                rebootBody = {
                    "uid": self.uid,
                    "clusterId": clusterId,
                    "deviceId": deviceId,
                    "is_only_lc": 1
                }
                url = REQUEST_URL + "/api/ops/rebootAll"

                for i in range(DEVICE_REBOOT_TIMES):
                    resposne = requests.post(url=url, data=json.dumps(rebootBody), headers=headers, verify=False)
                    resposne = resposne.content.decode('UTF-8')
                    resposne = json.loads(resposne)

                    rebootStatus = response.get('status').get('res')
                    rebootError = response.get('message').get('error')
                    if not rebootStatus:
                        print( "第%d次重启失败：%s;失败日志: %s" % (i, str(deviceId), str(rebootError)) )
                        if i == (int(DEVICE_REBOOT_TIMES) - 1):
                            result['error'] = "设备%s重启多次失败!" % deviceId 
                            return result

                    break

        # 最终判断是否有异常
        if not result['error']:
            result['status'] = True

        print("result========================")
        pprint(result)
        return result