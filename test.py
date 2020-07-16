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
#     "ports": [22,3000,3306,4200,8270],
#     "node_labels": {
#         "app" : "jenkins",
#     }
}]

depNames = [
"xn-autotest-sdkus01bc9af851c4bdc8125ce552dcd4a910",
"xn-autotest-sdkus0982084133d5aa100763302094fbe38d",
"xn-autotest-sdkus12a1b95e3373113d2aaa8a0d89f54f0f",
"xn-autotest-sdkus2c7d9a7e095c29fdb118cac8d96452a5",
"xn-autotest-sdkus30cb4acd887fd696569d7f4674105f37",
"xn-autotest-sdkus3391c7dd145281e17989983e454e4eb8",
"xn-autotest-sdkus34c8ceda10b6dbe3325b75aa4000671f",
"xn-autotest-sdkus4c58492d339c3e0415fced66141f080b",
"xn-autotest-sdkus51927935735fd0e906c12eb6d5e6e69f",
"xn-autotest-sdkus55c3f0d676565f0843f929a575208433",
"xn-autotest-sdkus6547a42e3f82f9a074ae7e1fae8fd0f3",
"xn-autotest-sdkus67f415a568c9b2628ea54973c6265064",
"xn-autotest-sdkus6adaedb4fea1989abdd637d7ab95a597",
"xn-autotest-sdkus6b6770c59e27938e3cfea0131f4068db",
"xn-autotest-sdkus6ea9ab41d9a4d886459aae301df97dc1",
"xn-autotest-sdkus81f96cdb0e9a2e7e8447d4f74d7c4acc",
"xn-autotest-sdkus925fcfdee42de91910db8a5e5b8fe1c6",
"xn-autotest-sdkus92889d1a2809011ffba271fabded70e7",
"xn-autotest-sdkus99e77a880e65a4185eec4e8e47714a0b",
"xn-autotest-sdkus9a160a94ab6924227f3ec779c3ca6eb8",
"xn-autotest-sdkus9f5ab3021fb9b878aeb41ee26f8d7046",
"xn-autotest-sdkusa61d384d825f613ad47431b7f9bd28d8",
"xn-autotest-sdkusaf94d4d347868411a4c8962e19115698",
"xn-autotest-sdkusb01445ead7c4fd57324e25a2c0c97ee5",
"xn-autotest-sdkusb882860833e67abad9ac7413d1242f4f",
"xn-autotest-sdkusb925903609572bfcc78cc7d321997d2c",
"xn-autotest-sdkuscc929ec76b68356c371f50deb5aba4da",
"xn-autotest-sdkusd7bc7746dc18c008647a09bf5564eee3",
"xn-autotest-sdkusdbb8d04eb833bd450c99ce3a9c4dce37",
"xn-autotest-sdkusdfb54fd947c30f84d3a9a32704e8e3bf",
"xn-autotest-sdkuseee2d1bddc90a2fdf3ce491c6cdaa27f",
"xn-autotest-sdkusf79c4e3152b8c78b8c0967445684a884",
"xn-autotest-sdkusfd3856cd62a70495cecafe960c5944e0",
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