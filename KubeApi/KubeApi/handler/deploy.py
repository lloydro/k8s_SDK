
import json
from typing import List
from pprint import pprint
from kubernetes import client, config
from os import path
from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException
import time
from kubernetes.stream import stream
import hashlib
import uuid
import random
import math
import re
from KubeApi.config.settings import REQUEST_URL,POD_IP_TIMES,POD_IP_DELAY
import requests



class DeployHandler(object):
    '''
    K8s deployment operator.

    ::

        >>> from KubeApi.api import ApiHandler

    '''

    def __init__(
        self,
        uid
        ):
        self.uid = uid

    
    '''
    create one k8s deployments or more. （创建容器）

    ::
    
        >>> Request example:

        configList:[{
            "image" : 'docker-hub.ruijie.work/base_project/bfn-rf:latest',
            "command" : '/usr/bin/AutoStart',
            "cpu" : 500,
            "memory" : 200,
            "ephemeral_storage" : 10,
            "ports": "22,3000,3306,4200,8270",
            "node_labels": {
                "app" : "jenkins",
            },
        }]


        >>> Response example:
        {
            'datas': {
                'node': 'node12',
                'deps': {
                    'xn-autotest-hanch609badc9949011c53c8aa480de7bbb0e': {
                        'name': 'xn-autotest-hanch609badc9949011c53c8aa480de7bbb0e',
                        'deploy_name': 'xn-autotest-hanch609badc9949011c53c8aa480de7bbb0e',
                        'service_name': 'xn-autotest-hanch609badc9949011c53c8aa480de7bbb0e',
                        'host_ip': '172.29.46.195',
                        'pod_ip': '10.0.1.1',
                        'mysql_port': 47250,
                        'ssh_port': 61755,
                        'web_ssh_port': 51304,
                        'error': '',
                        'res': True
                    }
                }
            },
            'error': '',
            'status': True
        }

    '''
    def create_deps(self,configList):


        result = {
            'datas': {
                'node': '',
                'deps':{}
            },
            'error': '',
            'status': True
        }

        # 过滤出来的属性
        result_deps_pool = ['name','deploy_name','service_name','host_ip','rf_port','mysql_port','ssh_port','pod_ip','web_ssh_port','port_map','error','res']

        reqData = []
        
        for config in configList:
            
            # 端口数据转字符串
            for i in range( len(config.get('ports')) ):
                config.get('ports')[i] = str(config.get('ports')[i]) 

            reqData.append({
                "id": uuid.uuid4().__str__(),
                "uid": self.uid,
                "image": config.get('image'),
                "label": '', 
                "name": 'sdkuser',
                "command": config.get('command'), 
                "cpu": config.get('cpu'), 
                "memory": config.get('memory'), 
                "ephemeral_storage": config.get('ephemeral_storage'), 
                "ports": ','.join(config.get('ports')), 
                "is_build": 0,
                "is_persistent": 0,
                "p_name": '',
                "p_path": '',
                "p_storage": 0,
                "sub_net_name": [],
                "node_name": '',
                "pic": '',
                "coordinate": [],
                "is_set": -1,
                "node_labels": config.get('node_labels')
            })
        
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "python-requests/2.9.1",
        }
        url = REQUEST_URL + "/api/multiDeploy"
        response = requests.post(url=url, data=json.dumps(reqData), headers=headers, verify=False)
        response = response.content.decode('UTF-8')
        response = json.loads(response)

        # pprint(response)

        datas = response.get('data')

        status = response.get('status')

        # print(status)
        if status:
            for k,v in status.items():
                if v == False:
                    result['error'] = '容器创建过程出错'
                    result['status'] = False
                    break
        # print('===========================')

        # 容器创建都成功
        if result['status'] == True:
            # 调整result结构

            id_to_name_map = {} # id与name的映射关系
            podNames = [] # 容器name列表，获取pod_ip时候用
            
            result.get("datas")["node"] = datas.get('node')

            # 构造容器属性body，并补充map列表
            for id,name in datas.get('name').items():
                result.get("datas").get("deps")[name] = {}
                id_to_name_map[id] = name 
                podNames.append(name)

            # 填充容器属性
            for k,v in datas.items():
                if k in result_deps_pool:
                    for dep_id,dep_val in v.items():
                        dep_name = id_to_name_map[dep_id]
                        if dep_name:
                            result.get("datas").get("deps")[dep_name][k] = dep_val

            # pprint(result)
            # print('++++++++++++++++++++++++++++++++++')
            # get pod_ip 
            # 添加podIp
            url = REQUEST_URL + "/api/getPodIps"
            for i in range(POD_IP_TIMES):
                time.sleep(POD_IP_DELAY)
                res = requests.post(url=url, data=json.dumps(podNames), headers=headers, verify=False)
                res = res.content.decode('UTF-8')
                res = json.loads(res)
                # print('get_pod_res====================',res)
                if res.get('status') == True:
                    pod_ips = res.get('datas')
                    for name,props in result.get("datas").get("deps").items():
                        result.get("datas").get("deps")[name]['pod_ip'] = pod_ips[name]
                    break
            

            # 超出等待时间，需要删除未获取到pod_ip的容器，并抛异常
            delete_dep_list = []
            for d_name,d_item in result.get("datas").get("deps").items():
                # 有一个没得到pod_ip，就都删除
                if not d_item.get('pod_ip'):
                    if len(podNames) > 0:
                        for p_name in podNames:
                            delete_dep_list.append({
                                "name" : p_name
                            })
                        print('----------------部分容器未获得pod_ip，需要删除所有容器:-----------------------:')
                        print(podNames)
                        delete_res = self.delete_deps(delete_dep_list)
                        print('----------------删除结果-------------------:')
                        print(delete_res)
                        # TODO.清空result数据
                        result = {
                            'datas': {
                                'node': '',
                                'deps':{}
                            },
                            'error': '',
                            'status': True
                        }
                        result['error'] = '创建失败，容器启动异常导致部分pod_ip未获取到，请确认配置'
                        result['status'] = False
                        # raise Exception("创建失败，容器启动异常导致部分pod_ip未获取到，请确认配置")
                    
        # pprint(result)
        return result




    '''
    delete one k8s deployments or more. （删除容器）

    ::
    
        >>>  Request example:

        depList = [{
            "name" : 'xn-autotest-hanch27e23072e1fefe083906563cf0fc8cb1',
        }]

        >>> Response example:
        {
            'datas': {
                'node': '',
                'deps': {
                    'xn-autotest-hanch609badc9949011c53c8aa480de7bbb0e': {
                        'error': '',
                        'deleteRes': True
                    }
                }
            },
            'error': '',
            'status': True
        }

    '''
    def delete_deps(self,depList):

        result = {
            'datas': {
                'node': '',
                'deps':{}
            },
            'error': '',
            'status': True
        }

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "python-requests/2.9.1",
        }

        # 构造请求
        reqData = []
        for dep in depList:
            reqData.append({
                'id': '',
                'uid': self.uid,
                'name': dep.get('name'),
                'is_set': -1
            })

        url = REQUEST_URL + "/api/delDeploy"
        response = requests.post(url=url, data=json.dumps(reqData), headers=headers, verify=False)
        response = response.content.decode('UTF-8')

        response = json.loads(response)

        result['datas'] = response.get('data')
        if result.get('datas').get('deps'):
            for k,v in result.get('datas').get('deps').items():
                if v.get('deleteRes') == False:
                    result['error'] = '容器删除过程出错'
                    result['status'] = False
                    break

        # pprint(result)
        return result



            