
from KubeApi.handler.deploy import DeployHandler
from KubeApi.handler.server import ServerHandler

class KubeClient(object):

    def __init__(self,uid):
        self.uid = uid


    '''
    handle the operation. 

    ::
        augment statements:

        resource_type => 操作的资源类型，例如deployment
        handle_type => 操作的方法，例如 CREATE、DELETE、QUERY
        datas => 配置参数，详见对应的方法定义
    
        >>> example:

        kubeClient.handle('deployment','CREATE',configList)

    '''
    def handle(self, resource_type, handle_type, datas = '' ):

        result = {
            'error': '方法不存在: ' + handle_type + ' -> '+ handle_type,
            'status': False
        }

        if resource_type == 'deployment' and handle_type == 'CREATE':
            handler = DeployHandler(self.uid)
            result = handler.create_deps(datas)
        
        if resource_type == 'deployment' and handle_type == 'DELETE':
            handler = DeployHandler(self.uid)
            result = handler.delete_deps(datas)

        if resource_type == 'deployment' and handle_type == 'GET_NAMES':
            handler = DeployHandler(self.uid)
            result = handler.get_pod_list()

        if resource_type == 'deployment' and handle_type == 'GET_DEPS_BY_UID':
            handler = DeployHandler(self.uid)
            result = handler.get_deps_by_uid()
        
        if resource_type == 'server' and handle_type == 'CREATE_TOPO_BY_TEMP':
            handler = ServerHandler(self.uid)
            result = handler.create_ops_topo_by_template_id(datas)

        return result