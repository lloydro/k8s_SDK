from KubeApi.app import KubeClient
import _thread
THREAD_NUM = 1

is_create_ops_topo_by_id = True
is_get_pod_by_uid = False
is_get_pod_list = False
is_create = False

uid = 'han_chen'


templateCfg = {
    "templateId": "5cb88725-2ebf-4342-ab45-6512505739ff",
    "topoName": "tp1.top",
    "topoLifeDays": 30
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

for i in range(THREAD_NUM):
    if is_create_ops_topo_by_id:
        _thread.start_new_thread(createOpsTopoByTempId,(),)
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