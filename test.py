from KubeApi.app import KubeClient
import _thread
THREAD_NUM = 1

is_create_ops_topo_by_id = False
is_switch_ops_topo = True
is_get_pod_by_uid = False
is_get_pod_list = False
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
    "node_name": "kolla-compute18",
    "topoId": "5c5728b2-dc63-46d9-b344-800363ac125b",
    "topoName": "switchTest", 
    "newTopo": {
        "b63c1f80-3fbf-4c5a-8334-90402c4bd7d5" : [ 
            "23de15de-1e7b-4eb1-a9ea-f6f6ed99ca48",
            "c05e0728-a5ea-4ac8-95dd-73d4f049ecb7"
        ],
        "6477c937-e2eb-4af3-a46f-17ed6f0f2216" : [ 
            "c05e0728-a5ea-4ac8-95dd-73d4f049ecb7"
        ],
    },
    "is_reboot_exp": 1
}


configList = [{
    "image": "docker-hub.ruijie.work/base_project/robotframework-12.5pl1:latest",
    "command": '/usr/bin/AutoStart',
    "cpu": 1024,
    "memory": 4096,
    "ephemeral_storage": 10,
    "node_labels": {
        "app": "jenkins",
    },
    "ports": [22, 3306, 4200, 8270],
    "is_resource_occupied": True,
    "is_count": 1,
    "max_count": 2,
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
"xn-autotest-sdkus157267fa8234e991767bd91084fbd73a",
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
    else:
        if is_create:
            _thread.start_new_thread(createDeps,(),)
        else:
            _thread.start_new_thread(deleteDeps,(),)


while(True):
    pass