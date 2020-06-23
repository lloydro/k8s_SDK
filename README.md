
上传：
python setup.py sdist upload -r privatepypi 

安装：
pip3 install --upgrade -i http://172.18.34.10:3141 --trusted-host 172.18.34.10  KubeApi


使用示例：

from KubeApi.app import KubeClient   # 引用SDK
createData = [{                      # 构造参数
    "image" : 'docker-hub.ruijie.work/base_project/bfn-rf:latest',
    "command" : '/usr/bin/AutoStart',
    "cpu" : 500,
    "memory" : 200,
    "ephemeral_storage" : 10,
    "ports": [22,3000,3306,4200,8270]
}]
kubeClient = KubeClient(uid)    
kubeClient.handle('deployment','CREATE',createData)     # 创建容器


详细说明文档地址：
http://conf.ruijie.work/pages/viewpage.action?pageId=51645745