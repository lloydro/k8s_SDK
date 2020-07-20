from KubeApi.app import KubeClient
import _thread
THREAD_NUM = 1

is_create = True

uid = 'han_chen'

configList = [{
    'image': 'docker-hub.ruijie.work/base_project/robotframework-branch_12.5pl1:latest',
	'command': '/usr/bin/AutoStart',
	'cpu': 1000,
	'memory': 2048,
	'ephemeral_storage': 10,
	'ports': [22, 3000, 3306, 4200, 8270],
    # "node_labels": {
    #     "app" : "jenkins",
    # }
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
"xn-autotest-sdkus182bc34494ea546dec714b2a707d5601",
"xn-autotest-sdkus8ad0214779d99e2f0801571ef7ba6b1f",
"xn-autotest-sdkusa7b5f9ec4395055bc64b7539ec04a8e8",
"xn-autotest-sdkusb75a0196c79e14103413754bfa525b77",
]


depList = []
for name in depNames:
    depList.append({
        "name" : name
    })

# depList = [{
#     "name" : 'xn-autotest-hanch7133fa325b6b8c6b2511c26237806eb1',
# },{
#     "name" : 'xn-autotest-hanch714575f10a5adc59be2fe178de8eb6ca',
# },{
#     "name" : 'xn-autotest-hanch715fe85ece1e2ca836c64492d5e49bb0',
# },{
#     "name" : 'xn-autotest-hanch7555f934d44726b5bb67a27f7c684352',
# },{
#     "name" : 'xn-autotest-hanchdb83a9170535b51f2a94866c6be59de5',
# },{
#     "name" : 'xn-autotest-hanchc5ba2af5168273d1fad519e3eff468b4',
# },{
#     "name" : 'xn-autotest-hanch8f74eb8012c715364b3b05dfde76927a',
# },{
#     "name" : 'xn-autotest-fanmec364d2b26bdf66885f1d500df00c7c9c',
# },{
#     "name" : 'xn-autotest-fanme426f4c2a00eb78815202f5576825a7dd',
# }]



def createDeps():
    kubeClient = KubeClient(uid)
    res = kubeClient.handle('deployment','CREATE',configList)
    print(res,type(res))



def deleteDeps():
    kubeClient = KubeClient(uid)
    res = kubeClient.handle('deployment','DELETE',depList)
    print(res,type(res))


for i in range(THREAD_NUM):
    if is_create:
        _thread.start_new_thread(createDeps,(),)
    else:
        _thread.start_new_thread(deleteDeps,(),)


while(True):
    pass