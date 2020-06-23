from KubeApi.app import KubeClient

is_create = True

uid = 'han-chen'

configList = [{
    "image" : 'docker-hub.ruijie.work/base_project/bfn-rf:latest',
    "command" : '/usr/bin/AutoStart',
    "cpu" : 500,
    "memory" : 200,
    "ephemeral_storage" : 10,
    "ports": [22,3000,3306,4200,8270]
}]

depList = [{
    "name" : 'xn-autotest-hancha52cd23296b54f39969448e30272dd3d',
}]

kubeClient = KubeClient(uid)

if is_create:
    print(kubeClient.handle('deployment','CREATE',configList))
else:
    print(kubeClient.handle('deployment','DELETE',depList))