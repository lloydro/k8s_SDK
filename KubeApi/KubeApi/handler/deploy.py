
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
from KubeApi.utils.kubeTask import KubeTask
from KubeApi.utils.utils import datetime_now,nomalize_unit,random_int,get_namespace
from KubeApi.config.settings import POD_IP_DELAY,POD_IP_TIMES



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
        self.cnn = KubeTask()
        self.node_pool = ['node05','node06','node07','node08','node09','node10','node11','node12','node13','node14','node15','node16','node17']


    
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
        # define result body
        result = {
            'datas': {
                'node': '',
                'deps':{}
            },
            'error': '',
            'status': True
        }

        # 检测入参：
        if type(configList) != list:
            result['error'] = '参数必须为list类型'
            print("DeployHandler >>>>> create_deps >>>>>>> the augment should be a list ")
            result["status"] = False
            return result
        
        # node_labels参数, 不传参则默认为jenkins
        node_labels = {
            "app" : "jenkins",
        }
        if configList[0].get("node_labels"):
            node_labels = configList[0].get("node_labels") 

        node_name_list = []    
        node_name_list_for_local_test = []
        # 匹配node_name
        nodes = self.cnn.list_nodes().items
        for node in nodes:
            labels = node.metadata.labels
            for k,v in node_labels.items():
                if node.metadata.name.find('node') != -1 and labels.get(k) == v:
                    node_name_list.append(node.metadata.name)
            if node.metadata.name.find('node') != -1  and labels.get('app') == 'local_test': # 收集local_test的name
                node_name_list_for_local_test.append(node.metadata.name)

        # 指定node，若未匹配上，则采用local_test
        if len(node_name_list) <=0:
            node_name_list = node_name_list_for_local_test

        node_idx = random_int(len(node_name_list))
        node_name = node_name_list[node_idx]

        print("node_name_list ========================================:",node_name_list)

        print("DeployHandler >>>>> create_deps >>>>>>> line 79 >>>>>> node is: ",node_name)
        node_selector = {
            "kubernetes.io/hostname": node_name
        }
        result.get('datas')['node'] = node_name


        for config in configList:
            body_name = self.uid.replace('-', '').replace('_','')
            checkRes = self.__checkInput(config,funcName='create_deps')
            if not checkRes['status']:
                result['error'] = checkRes['error']
                print("DeployHandler >>>>> create_deps >>>>>>> " + checkRes['error'])
                result["status"] = False
                return result
            
            image = config.get("image")
            command = config.get("command").split(",") # get command list
            for index in range(len(command)):
                command[index] = command[index].strip() # strip the space both side
            portList = config.get("ports")
            # 资源配置参数处理
            cpu = str(config.get("cpu")) + "m"
            memory = str(config.get("memory")) + "Mi"
            ephemeral_storage = str(config.get("ephemeral_storage")) + "G"
            limit_cpu = str(config.get("cpu") * 1.5) + "m"
            limit_memory = str(config.get("memory") * 1.5) + "Mi"
            limit_ephemeral_storage = str(config.get("ephemeral_storage") * 1.5) + "G"

            ms_service_name = int(time.time() * 1000)
            ms_service_name = str(ms_service_name)
            ms_timestamp = uuid.uuid4().__str__()
            ms_timestamp = ms_timestamp.replace('-', '')
            ms_timestamp = ms_service_name + ms_timestamp
            md = hashlib.md5()
            md.update(ms_timestamp.encode('utf-8'))
            ms_timestamp = md.hexdigest()

            if body_name:
                if len(body_name)>=5:
                    body_name=body_name[0:5]
                if '-' in str(body_name) or '_' in str(body_name) or not str(body_name).islower():
                    result['error'] = 'uid长度必须大于5'
                    print("DeployHandler >>>>> create_deps >>>>>>> " + result['error'])
                    result["status"] = False
                    return result

                body_name = str(body_name).lower()
                ms_timestamp = str(body_name) + ms_timestamp
            sub_name = 'xn-autotest-%s' % (ms_timestamp)
            namespace = get_namespace(self.uid)
            print("DeployHandler >>>>> create_deps >>>>>>> namespace is :",namespace)
            name = sub_name
            deploy_body = {
                    "kind": "Deployment",
                    "apiVersion": "apps/v1beta1",
                    "metadata": {
                        "name": name,
                        "namespace": namespace,
                        "labels": {
                            "k8s-app": name
                        },
                    },
                    "spec": {
                        "replicas": 1,
                        "selector": {
                            "matchLabels": {
                                "k8s-app": name
                            }
                        },
                        "template": {
                            "metadata": {
                                "name": name,
                                "labels": {
                                    "k8s-app": name
                                }
                            },
                            "spec": {
                                "containers": [{
                                    "name": name,
                                    "image": image,
                                    "command":  command,
                                    "resources": {
                                        "requests": {
                                            "cpu": cpu,
                                            "memory": memory,
                                            "ephemeral-storage": ephemeral_storage
                                        },
                                        "limits": {
                                            "cpu": limit_cpu,
                                            "memory": limit_memory,
                                            "ephemeral-storage": limit_ephemeral_storage
                                        }
                                    },
                                    "imagePullPolicy": "Always",
                                    "securityContext": {
                                        "privileged": True
                                    }
                                }],
                                "restartPolicy": "Always",
                                "node_selector": node_selector
                            }
                        }
                    }
                }
            
            # 对锐捷镜像，需要额外添加Secret配置
            if image.find("hub.ruijie") != -1:
                deploy_body["spec"]["template"]["spec"]["image_pull_secrets"] = [{"name": "myregcred"}]

            # ports列表对象构造
            portsArr = []
            for port in portList:
                port = str(port)
                portsArr.append({
                    "name": "tcp-" + port + "-" + port + "-" + ms_service_name,
                    "protocol": "TCP",
                    "port": int(port),
                    "targetPort": int(port)
                })
            
            service_body = {
                    "kind": "Service",
                    "apiVersion": "v1",
                    "metadata": {
                        "name": name,
                        "namespace": namespace,
                        "labels": {
                            "k8s-app": name
                        }
                    },
                    "spec": {
                        "ports": portsArr,
                        "selector": {
                            "k8s-app": name
                        },
                        "type":"NodePort"
                    }
                }

            deploy_body = json.dumps(deploy_body, indent=4)
            service_body = json.dumps(service_body, indent=4)

            deploy_name = sub_name
            service_name = sub_name

            # add data to result list
            result.get('datas').get('deps')[name] = {}
            result.get('datas').get('deps')[name]['name'] = name
            result.get('datas').get('deps')[name]['deploy_name'] = deploy_name
            result.get('datas').get('deps')[name]['service_name'] = service_name
            port_dict = {"mysql": None, "ssh": None, "web_ssh": None}
            _request_timeout = (7200, 7200)
            
            try:
                dep_status = self.cnn.create_container_with_deploy(deploy_body,_request_timeout=_request_timeout)
                # print(ms_timestamp+' create_container_with_deploy '+ str(deploy_body)+str(dep_status))
                host_ip_info = self.__get_k8s_hosts()
                random.shuffle(host_ip_info)
                host_ip = host_ip_info[0]
                result.get('datas').get('deps')[name]['host_ip'] = host_ip
                ports = []
                for lock_time in range(10):
                    try:
                        svc_status, ports = self.cnn.create_service_deploy(service_body,_request_timeout=_request_timeout)
                        # print(ms_timestamp + ' ok create_service_deploy ' + str(service_body) + str(svc_status)
                        #             + 'LOCK_UN times:' + str(lock_time))
                        break
                    except Exception as e:
                        print(str(e))
                        time.sleep(5)
                        pass

                if ports !=[]:
                    for d_port in ports:
                        if d_port.port == 8270:
                            port_dict['rf'] = d_port.node_port
                        if d_port.port == 22:
                            port_dict['ssh'] = d_port.node_port
                        if d_port.port == 3306:
                            port_dict['mysql'] = d_port.node_port
                        if d_port.port == 3000:
                            port_dict['test'] = d_port.node_port
                        if d_port.port == 4200:
                            port_dict['web_ssh'] = d_port.node_port
                result.get('datas').get('deps')[name]['mysql_port'] = port_dict["mysql"]
                result.get('datas').get('deps')[name]['ssh_port'] = port_dict["ssh"]
                result.get('datas').get('deps')[name]['web_ssh_port'] = port_dict["web_ssh"]
                result.get('datas').get('deps')[name]['rf_port'] = port_dict["rf"]
                result.get('datas').get('deps')[name]['error'] = ""
                result.get('datas').get('deps')[name]['res'] = True
                print('%s  exe_testcase ok' % (name))
            except Exception as e:
                print('%s  exe_testcase 2 fail' % (name))
                print('create error except error'+str(e))
                result.get('datas').get('deps')[name]['res'] = False
                result.get('datas').get('deps')[name]['error'] = str(e)
                result["error"] = '容器创建过程出错'
                result["status"] = False
        
        # 添加podIp
        for i in range(POD_IP_TIMES):
            leng = 0 
            time.sleep(POD_IP_DELAY)
            pod_list = self.cnn.list_namespaced_pod(namespace)
            # print(pod_list)
            for name,body in result.get('datas').get('deps').items():
                for pod in pod_list.items:
                    if pod.metadata.name.find(name) != -1:
                        pod_ip = pod.status.pod_ip
                        print("get pod_ip, leng, name ====================",pod_ip,type(pod_ip),leng, name)
                        if pod_ip != None:
                            body['pod_ip'] = pod_ip
                            leng += 1
                            break

            if leng == len(configList):
                print("leng,len(configList) ====================",leng,len(configList))
                break


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

        # 检测入参：
        if type(depList) != list:
            result['error'] = '参数必须为list类型'
            print("DeployHandler >>>>> delete_deps >>>>>>> the augment should be a list ")
            result["status"] = False
            return result

        for dep in depList:

            checkRes = self.__checkInput(dep,funcName='delete_deps')
            if not checkRes['status']:
                result['error'] = checkRes['error']
                print("DeployHandler >>>>> delete_deps >>>>>>> " + checkRes['error'])
                result["status"] = False
                return result

            name = dep.get("name")
            namespace = get_namespace(self.uid)
            result.get('datas').get('deps')[name] = {}

            try:
                deploy_body={'metadata':{'name':name,'namespace':namespace}}
                svc_body = deploy_body
                del_dep_status,del_svc_status = self.__delete_dep_svc (name, deploy_body, svc_body)

                result.get('datas').get('deps')[name]['error'] = ""
                result.get('datas').get('deps')[name]['deleteRes'] = True
                print('%s delete exe_testcase ok' % (name))
            except Exception as e:
                print('%s  exe_testcase 2 fail' % (name))
                print('delete error except error'+str(e))
                result.get('datas').get('deps')[name]['deleteRes'] = False
                result.get('datas').get('deps')[name]['error'] = str(e)
                result["error"] = '容器删除过程出错'
                result["status"] = False
        return result





    '''
     ----------------------------  private func  ----------------------------------------------
    '''

    # 删除deployment及svc
    def __delete_dep_svc(self,name,deploy_body,svc_body=None,_request_timeout=(3600,3600)):
        cnn = KubeTask()
        del_dep_status = False
        del_svc_status = False
        if svc_body:
            del_svc_status = cnn.delete_service_deploy(svc_body,config_file=None,context=None,_request_timeout=_request_timeout)
            # print(name + ' delete_service ' + str(svc_body) + str(del_svc_status))
        del_dep_status = cnn.delete_container_with_deploy(deploy_body,config_file=None,context=None,_request_timeout=_request_timeout)
        # print(name + ' delete_container_with_deploy ' + str(deploy_body) + str(del_dep_status))
        return del_dep_status,del_svc_status

    # 获取NODE IP
    def __get_k8s_hosts(self):
        nodes = self.cnn.list_nodes().items
        host_ip_info = []
        nodes_list = []
        for node in nodes:
            public_ip = node.metadata.annotations.get('flannel.alpha.coreos.com/public-ip')
            host_ip_info.append(public_ip)
            addresses = node.status.addresses
            inter_ip = ''
            host_name = ''
            node_status = 0
            for addresse in addresses:
                if addresse.type == 'InternalIP':
                    inter_ip = addresse.address
                if addresse.type == 'Hostname':
                    host_name = addresse.address
            for condition in node.status.conditions:
                if condition.type == 'Ready':
                    node_status = condition.status
                    if node_status == 'True':
                        node_status = 1
                    else:
                        node_status = 0
            nodes_list.append({"host_name": host_name, 'inter_ip': inter_ip, 'node_status': node_status,
                            'public_ip': public_ip})
        return host_ip_info 

    # 入参检测
    def __checkInput(self,data,funcName):
        res = {
            'error' : '',
            'status' : False    
        }

        if funcName == 'create_deps':

            if type(data) != dict:
                res['error'] = '列表项必须为字典'
                return res

            if not data.get('image'):
                res['error'] = 'image参数为空'
                return res
            
            if not data.get('command'):
                res['error'] = 'command参数为空'
                return res

            if not data.get('cpu'):
                res['error'] = 'cpu参数为空'
                return res
            
            if not data.get('memory'):
                res['error'] = 'memory参数为空'
                return res
            
            if not data.get('ephemeral_storage'):
                res['error'] = 'ephemeral_storage参数为空'
                return res
            
            if not data.get('ports'):
                res['error'] = 'ports参数为空'
                return res

            if type(data.get('ports')) != list:
                res['error'] = 'ports参数必须是列表'
                return res

        if funcName == 'delete_deps':

            if type(data) != dict:
                res['error'] = '列表项必须为字典'
                return res

            if not data.get('name'):
                res['error'] = 'name参数为空'
                return res

        res['status'] = True
        return res

            