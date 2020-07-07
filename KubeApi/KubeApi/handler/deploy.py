
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
from KubeApi.config.settings import REQUEST_URL
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
        data = {
            'uid': self.uid,
            'configList': configList
        }

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "python-requests/2.9.1",
        }
        url = REQUEST_URL + "/api/createDepsSDK"
        result = requests.post(url=url, data=json.dumps(data), headers=headers, verify=False)
        result = json.loads(result.content)
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
        data = {
            'uid': self.uid,
            'depList': depList
        }

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "python-requests/2.9.1",
        }
        url = REQUEST_URL + "/api/deleteDepsSDK"
        result = requests.post(url=url, data=json.dumps(data), headers=headers, verify=False)
        result = json.loads(result.content)
        # pprint(result)
        return result



            