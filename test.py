from KubeApi.app import KubeClient
import _thread
THREAD_NUM = 1

is_create_ops_topo_by_id = False
is_switch_ops_topo = False
is_get_pod_by_uid = False
is_get_pod_list = False
is_get_pods_ip = True
is_create = False

uid = 'han_chen'


templateCfg = {
    "templateId": "6fa45f24-d6de-43cb-95bb-5843524dd59c",
    "topoName": "switchTst",
    "topoLifeDays": 30000,
    "app_type": "switchtest"
}


# 'netList': {
#     'net1': '23de15de-1e7b-4eb1-a9ea-f6f6ed99ca48',
#     'net2': 'fa20c820-db1f-4838-b609-86b5028eb43b',
#     'net3': 'c05e0728-a5ea-4ac8-95dd-73d4f049ecb7'
# }
switchCfg = {
    "clusterId": 1,
    "node_name": "kolla-compute07",
    "topoId": "9d854417-c024-447f-942a-1735818ac4e1",
    "topoName": "autotest", 
    "newTopo": {
        "a77241c3-695e-4a11-841b-c0fcd5105b75" : [
            "64b238fc-17e0-4076-9cda-84995f3ba530",     # 本次拓扑连接关系
            "0e740209-2d2e-4d12-951c-a0502268b0f3",
            "47b915ae-035a-41cc-9628-1a8121a4ad84",
            "711c46c1-4f3c-4772-a245-55a2b08445c2",
            # "9f0d4d0d-87c2-43c2-a6f9-0d803d17c8c0"
        ],
        "6534ec0e-8f9d-4f62-96f5-c76453f530ce" : [
            "70ed59f1-596e-4cc6-97c5-211ab95fe046",
            "7ea53408-d514-4e5a-8cec-f6d8f3b88b38",
            "47b915ae-035a-41cc-9628-1a8121a4ad84",
            "711c46c1-4f3c-4772-a245-55a2b08445c2",
            # "9f0d4d0d-87c2-43c2-a6f9-0d803d17c8c0"
        ],
        # "b573708f-89c6-46fe-8d8f-4267276527f7" : [
        #     "64b238fc-17e0-4076-9cda-84995f3ba530",
        #     "0e740209-2d2e-4d12-951c-a0502268b0f3",
        #     "70ed59f1-596e-4cc6-97c5-211ab95fe046",
        #     "7ea53408-d514-4e5a-8cec-f6d8f3b88b38"
        # ],
    },
    "is_reboot_exp": 1
}


configList = [{
    "image" : 'docker-hub.ruijie.work/base_project/bfn-rf:latest',
    "command" : '/usr/bin/AutoStart',
    "cpu" : 500,
    "memory" : 200,
    "ephemeral_storage" : 10,
    "ports": [22,3000,3306,4200,8270],
    "node_labels": {
         "app" : "local_test"
    },
    # "image": "docker-hub.ruijie.work/base_project/robotframework-12.5pl1:latest",
    # "command": '/usr/bin/AutoStart',
    # "cpu": 1024,
    # "memory": 4096,
    # "ephemeral_storage": 10,
    # "node_labels": {
    #     "app": "jenkins",
    # },
    # "ports": [22, 3306, 4200, 8270],
    # "is_resource_occupied": True,
    # "is_count": 1,
    # "max_count": 2,
# },{
#     "image" : 'docker-hub.ruijie.work/base_project/bfn-rf:latest',
#     "command" : '/usr/bin/AutoStart',
#     "cpu" : 500,
#     "memory" : 200,
#     "ephemeral_storage" : 10,
#     "ports": [22,3000,3306,4200,8270],
    # "node_labels": {
    #     "app" : "jenkins",
    # }
}]

depNames = [
'xn-autotest-sdkusceb56fbc74f0c4fac8d110ee97e6d167',
'xn-autotest-sdkus8e266368ea2534b4a59c679b33064f66',
]


depList = []
for name in depNames:
    depList.append({
        "name" : name
    })

def createDeps():
    kubeClient = KubeClient(uid)
    res = kubeClient.handle('deployment','CREATE',configList)
    print(res,type(res))



def deleteDeps():
    kubeClient = KubeClient(uid)
    res = kubeClient.handle('deployment','DELETE',depList)
    print(res,type(res))


def getPodList():
    kubeClient = KubeClient(uid)
    res = kubeClient.handle('deployment','GET_NAMES')
    print(res,type(res))

def getPodsIp():
    kubeClient = KubeClient(uid)
    res = kubeClient.handle('deployment','GET_PODS_IP',depNames)
    print(res,type(res))

def getPodByUid():
    kubeClient = KubeClient(uid)
    res = kubeClient.handle('deployment','GET_DEPS_BY_UID')
    print(res,type(res))

def createOpsTopoByTempId():
    kubeClient = KubeClient(uid)
    res = kubeClient.handle('server','CREATE_TOPO_BY_TEMP',templateCfg)
    print(res,type(res))

def switchOpsTopo():
    kubeClient = KubeClient(uid)
    res = kubeClient.handle('server','SWITCH_TOPO',switchCfg)
    print(res,type(res))

for i in range(THREAD_NUM):
    if is_create_ops_topo_by_id:
        _thread.start_new_thread(createOpsTopoByTempId,(),)
    elif is_switch_ops_topo:
        _thread.start_new_thread(switchOpsTopo,(),)
    elif is_get_pod_by_uid:
        _thread.start_new_thread(getPodByUid,(),)
    elif is_get_pod_list:
        _thread.start_new_thread(getPodList,(),)
    elif is_get_pods_ip:
        _thread.start_new_thread(getPodsIp,(),)
    else:
        if is_create:
            _thread.start_new_thread(createDeps,(),)
        else:
            _thread.start_new_thread(deleteDeps,(),)


while(True):
    pass