from KubeApi.app import KubeClient
import _thread

THREAD_NUM = 1

is_create = True

uid = 'han-chen'

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
"xn-autotest-hanch1771f0aaff55311c791869a784dc0eb2",
"xn-autotest-hanch204b521379bdb711a86d382d9be1dc0c",
"xn-autotest-hanch238f6e4487f7d06ea06d05c16963fa63",
"xn-autotest-hanch24d29e38420f87a73612c2b88680816d",
"xn-autotest-hanch320cb218435daabe15156fbf042588c5",
"xn-autotest-hanch381efc443d7c1c74df305858ca0c5a54",
"xn-autotest-hanch44cb0ae6cbf036456ad4fbfd37adfe08",
"xn-autotest-hanch4704fa2259d8a63c828ef602f91870a3",
"xn-autotest-hanch484f88a6416b8df3f315e4ea62bf0373",
"xn-autotest-hanch48550fbc12c51041215ff629355af516",
"xn-autotest-hanch4a8342f01e8854c1185564f617239c86",
"xn-autotest-hanch4b264f09e540427434009fb33891bbf8",
"xn-autotest-hanch5c8c025417c64f1bf60fbb9c830cf87d",
"xn-autotest-hanch5c9f4f89bf3b83ff3c42c32416f3838b",
"xn-autotest-hanch649d3ad83bc6221f392adbe43b9f43e3",
"xn-autotest-hanch79e6dc94fa8a58e7c6a43dbcdfed1599",
"xn-autotest-hanch7aebf56a2fa25e95fd53bd6284b9aa51",
"xn-autotest-hanch889d911f4f8e5d15889f190d8b6d5abc",
"xn-autotest-hanch9060958c9d86f53ad742625808659adc",
"xn-autotest-hanch93140a494add3c64b42acf1fc48ddd27",
"xn-autotest-hanch9e673cd5375035828a67fe1f6bcde61b",
"xn-autotest-hancha613ab846e6e37b25d437ba83232299a",
"xn-autotest-hanchb683d8f927f270583443a601470ef0a5",
"xn-autotest-hanchbbc829658e568ed1f70c7d88578f77c6",
"xn-autotest-hanchcb47297d52d3f72f2903e416d0483cbf",
"xn-autotest-hanchf0fc098d21759a3a9bfb5d87c3e236bf",
"xn-autotest-hanchf369f9aa5990c7cf9319bab49a9c13a4",
"xn-autotest-hanchf697b1b81e4ad8404b07df737ea2cfdf",
"xn-autotest-hanchf7e6b034b9d21425ed73cb3d55549a4c",
"xn-autotest-hanchfbde8121dd9d07f0cbd5b077c05fa64f",
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