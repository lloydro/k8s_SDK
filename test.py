from KubeApi.app import KubeClient

is_create = False

uid = 'han-chen'

configList = [{
    "image" : 'docker-hub.ruijie.work/base_project/bfn-rf:latest',
    "command" : '/usr/bin/AutoStart',
    "cpu" : 500,
    "memory" : 200,
    "ephemeral_storage" : 10,
    "ports": [22,3000,3306,4200,8270],
    "node_labels": {
        "app" : "local_test",
    }
# },{
#     "image" : 'docker-hub.ruijie.work/base_project/bfn-rf:latest',
#     "command" : '/usr/bin/AutoStart',
#     "cpu" : 500,
#     "memory" : 200,
#     "ephemeral_storage" : 10,
#     "ports": [22,3000,3306,4200,8270]
}]

depList = [{
#     "name" : 'xn-autotest-hanch7133fa325b6b8c6b2511c26237806eb1',
# },{
#     "name" : 'xn-autotest-hanch714575f10a5adc59be2fe178de8eb6ca',
# },{
#     "name" : 'xn-autotest-hanch715fe85ece1e2ca836c64492d5e49bb0',
# },{
#     "name" : 'xn-autotest-hanch7555f934d44726b5bb67a27f7c684352',
# },{
#     "name" : 'xn-autotest-hanch781c8509bb9ef3501a8041dabc7f5231',
# },{
#     "name" : 'xn-autotest-hanch79a45572e3c4b0a25c1df8c99f1af5e1',
# },{
#     "name" : 'xn-autotest-hanchc5931a6c3730470e5ee98fc2b486626d',
# },{
#     "name" : 'xn-autotest-hanch6bc5e29dffec8727ad0e06c896f46ac9',
# },{
    "name" : 'xn-autotest-hanch713993df8289c256a416dd60f1e2cf2d',
}]


































kubeClient = KubeClient(uid)

if is_create:
    print(kubeClient.handle('deployment','CREATE',configList))
else:
    print(kubeClient.handle('deployment','DELETE',depList))