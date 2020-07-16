from KubeApi.app import KubeClient
import _thread
THREAD_NUM = 1

is_create = False

uid = 'han_chen'

configList = [{
    "image" : 'docker-hub.ruijie.work/base_project/bfn-rf:latest',
    "command" : '/usr/bin/AutoStart',
    "cpu" : 500,
    "memory" : 200,
    "ephemeral_storage" : 10,
    "ports": [22,3000,3306,4200,8270],
    "node_labels": {
        "app" : "jenkins",
    }
# },{
#     "image" : 'docker-hub.ruijie.work/base_project/bfn-rf:latest',
#     "command" : '/usr/bin/AutoStart',
#     "cpu" : 500,
#     "memory" : 200,
#     "ephemeral_storage" : 10,
#     "ports": [22,3000,3306,4200,8270]
}]

depNames = [
"xn-autotest-hanch0987d1792f5e59f0684918bc1050ed1b",
"xn-autotest-hanch0bdc4d1de7235ed2cae72e6f3b62c30f",
"xn-autotest-hanch3334235922a57eceb16c20711d763ce2",
"xn-autotest-hanch3d41a13d29d630099aa081a7d26d41bd",
"xn-autotest-hanch42b4ee611a10429398e884627b69f240",
"xn-autotest-hanch7687991e6d7f53d29ef1bdbe7d354fd0",
"xn-autotest-hanch97f770e21c791f0ce3d9ee4ab93f1cb8",
"xn-autotest-hanchb35db30821f5f7b0085e897e8ce8750c",
"xn-autotest-hanchbae92f4eb4bf2a34362f9a23df13b649",
"xn-autotest-hanchbf9781931b9bb8701dda8e4626cee41b",
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