

from pprint import pprint
from kubernetes import client, config
from os import path
from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException
import time
from kubernetes.stream import stream
import six
import requests
import json
# from config.settings import CNI_URL


class KubeExec(object):
    def __init__(self,config_file=None,context=None):
        if config_file and context:
            config.load_kube_config(config_file=config_file,context=context)
        else:
            config.load_kube_config()
        self.client = client
        self.apps_v1beta1 = self.client.AppsV1beta1Api()
        self.core_v1_api = client.CoreV1Api()
        self.apps_v1_api = client.AppsV1Api()
        self.extensions_v1_beta1_api = client.ExtensionsV1beta1Api(client.ApiClient())
        self.rbac_authorization_v1_api = client.RbacAuthorizationV1Api(client.ApiClient())
        self.rbac_authorization_v1_beta1_api = client.RbacAuthorizationV1beta1Api(client.ApiClient())
    
    def create_namespace(self,namespace,_request_timeout):
        try:
            metadata = self.client.V1ObjectMeta()
            metadata.name = namespace
            metadata.labels = {"name" : namespace}

            body = self.client.V1Namespace()
            body.api_version = "v1"
            body.kind = "Namespace"
            body.metadata = metadata

            # pprint(body)
            api_response = self.core_v1_api.create_namespace(body,_request_timeout=_request_timeout)
            # pprint(api_response)
            return True 
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespace: %s\n" % str(e))
            return False
    
    def create_service_account(self,namespace,_request_timeout):
        try:
            metadata = self.client.V1ObjectMeta()
            metadata.name = namespace
            metadata.namespace = namespace

            body = self.client.V1ServiceAccount()
            body.api_version = "v1"
            body.kind = "ServiceAccount"
            body.metadata = metadata

            # pprint(body)
            api_response = self.core_v1_api.create_namespaced_service_account(namespace,body,_request_timeout=_request_timeout)
            # pprint(api_response)
            return True 
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_service_account: %s\n" % str(e))
            return False

    def create_role(self,namespace,_request_timeout):
        try:
            metadata = self.client.V1ObjectMeta()
            metadata.name = "role-" + namespace
            metadata.namespace = namespace

            rules = [
                {
                        "apiGroups": [""],
                        "resources": ["pods"],
                        "verbs": ["get", "list", "watch", "delete","create", "update", "patch"]
                },{
                        "apiGroups": [""],
                        "resources": ["pods/portforward", "pods/proxy"],
                        "verbs": ["get", "list", "watch", "create", "update", "patch", "delete"]
                },{
                        "apiGroups": [""],
                        "resources": ["pods/log"],
                        "verbs": ["get", "list", "watch", "delete"]
                },{
                        "apiGroups": ["extensions", "apps"],
                        "resources": ["deployments"],
                        "verbs": ["get", "list", "watch", "create", "update", "patch", "delete"]
                },{
                        "apiGroups": [""],
                        "resources": ["namespaces"],
                        "verbs": ["get", "watch", "list"]
                },{
                        "apiGroups": [""],
                        "resources": ["events"],
                        "verbs": ["get", "watch", "list"]
                },{
                        "apiGroups": ["apps", "extensions"],
                        "resources": ["replicasets"],
                        "verbs": ["get", "watch", "list", "create", "update", "pathch", "delete"]
                },{
                        "apiGroups": [""],
                        "resources": ["configmaps"],
                        "verbs": ["get", "watch", "list", "create", "update", "pathch", "delete"]
                },{
                        "apiGroups": [""],
                        "resources": ["persistentvolumeclaims"],
                        "verbs": ["get", "watch", "list"]
                },{
                        "apiGroups": [""],
                        "resources": ["secrets"],
                        "verbs": ["get", "watch", "list"]
                },{
                        "apiGroups": [""],
                        "resources": ["services"],
                        "verbs": ["get", "watch", "list", "create", "update", "pathch", "delete"]
                },{
                        "apiGroups": ["extensions"],
                        "resources": ["ingresses"],
                        "verbs": ["get", "watch", "list","create","delete"]
                },{
                        "apiGroups": ["apps"],
                        "resources": ["daemonsets"],
                        "verbs": ["get", "watch", "list"]
                },{
                        "apiGroups": ["batch"],
                        "resources": ["jobs"],
                        "verbs": ["get", "watch", "list"]
                },{
                        "apiGroups": ["batch"],
                        "resources": ["cronjobs"],
                        "verbs": ["get", "watch", "list"]
                },{
                        "apiGroups": [""],
                        "resources": ["replicationcontrollers"],
                        "verbs": ["get", "watch", "list"]
                },{
                        "apiGroups": ["apps"],
                        "resources": ["statefulsets"],
                        "verbs": ["get", "watch", "list"]
                },{
                        "apiGroups": [""],
                        "resources": ["endpoints"],
                        "verbs": ["get", "watch", "list"]
                },{
                        "apiGroups": [""],
                        "resources": ["pods/exec"],
                        "verbs": ["get", "list", "watch","create"]
                },
            ]

            body = self.client.V1Role()
            body.api_version = "rbac.authorization.k8s.io/v1"
            body.kind = "Role"
            body.metadata = metadata
            body.rules = rules

            # pprint(body)
            api_response = self.rbac_authorization_v1_api.create_namespaced_role(namespace,body,_request_timeout=_request_timeout)
            # pprint(api_response)
            return True 
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_role: %s\n" % str(e))
            return False

    def create_role_binding(self,namespace,_request_timeout):
        try:
            r_api_group = "rbac.authorization.k8s.io"
            r_kind = "Role"
            r_name = "role-" + namespace
            role_ref = self.client.V1RoleRef( 
                api_group = r_api_group,
                kind = r_kind,
                name = r_name 
            )

            subjects = [
                {
                    "kind": "ServiceAccount",
                    "name": namespace,
                    "namespace": namespace
                },{
                    "kind": "User",
                    "name": namespace,
                    "namespace": namespace
                }
            ]

            metadata = self.client.V1ObjectMeta()
            metadata.name = "role-bind-" + namespace
            metadata.namespace = namespace

            body_api_version = "rbac.authorization.k8s.io/v1"
            body_kind = "RoleBinding"
            body_metadata = metadata
            body_role_ref = role_ref
            body_subjects = subjects
            body = self.client.V1RoleBinding( 
                api_version = body_api_version,
                kind = body_kind,
                metadata = body_metadata, 
                role_ref = body_role_ref,
                subjects = body_subjects
            )
            
            # pprint(body)
            api_response = self.rbac_authorization_v1_api.create_namespaced_role_binding(namespace,body,_request_timeout=_request_timeout)
            # pprint(api_response)
            return True 
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_role_binding: %s\n" % str(e))
            return False

    def create_cluster_role(self,namespace,_request_timeout):
        try:
            rules = [
                {
                        "apiGroups": [""],
                        "resources": ["secrets"],
                        "verbs": ["get", "watch", "list","create"]
                },{
                        "apiGroups": [""],
                        "resources": ["namespaces"],
                        "verbs": ["get", "watch", "list"]
                },{
                        "apiGroups": [""],
                        "resources": ["pods/exec"],
                        "verbs": ["get", "list", "watch","create"]
                }
            ]

            metadata = self.client.V1ObjectMeta()
            metadata.name = "cluster-role-" + namespace

            body_api_version = "rbac.authorization.k8s.io/v1beta1"
            body_kind = "ClusterRole"
            body_metadata = metadata
            body_rules = rules
            body = self.client.V1beta1ClusterRole( 
                api_version = body_api_version,
                kind = body_kind,
                metadata = body_metadata, 
                rules = body_rules
            )
            
            # pprint(body)
            api_response = self.rbac_authorization_v1_beta1_api.create_cluster_role(body,_request_timeout=_request_timeout)
            # pprint(api_response)
            return True 
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_cluster_role: %s\n" % str(e))
            return False

    def create_cluster_role_binding(self,namespace,_request_timeout):
        try:
            r_api_group = "rbac.authorization.k8s.io"
            r_kind = "ClusterRole"
            r_name = "cluster-role-" + namespace
            role_ref = self.client.V1RoleRef( 
                api_group = r_api_group,
                kind = r_kind,
                name = r_name 
            )

            subjects = [
                {
                    "kind": "ServiceAccount",
                    "name": namespace,
                    "namespace": namespace
                }
            ]

            metadata = self.client.V1ObjectMeta()
            metadata.name = "cluster-role-bind-" + namespace

            body_api_version = "rbac.authorization.k8s.io/v1beta1"
            body_kind = "ClusterRoleBinding"
            body_metadata = metadata
            body_role_ref = role_ref
            body_subjects = subjects
            body = self.client.V1beta1ClusterRoleBinding( 
                api_version = body_api_version,
                kind = body_kind,
                metadata = body_metadata, 
                role_ref = body_role_ref,
                subjects = body_subjects
            )
            
            # pprint(body)
            api_response = self.rbac_authorization_v1_beta1_api.create_cluster_role_binding(body,_request_timeout=_request_timeout)
            # pprint(api_response)
            return True 
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_cluster_role_binding: %s\n" % str(e))
            return False
    
    def create_secret(self,namespace,_request_timeout):
        try:
            metadata = self.client.V1ObjectMeta()
            metadata.name = "myregcred" 
            metadata.namespace = namespace

            body_api_version = "v1"
            body_kind = "Secret"
            body_data = { ".dockerconfigjson" : "eyJhdXRocyI6eyJkb2NrZXItaHViLnJ1aWppZS53b3JrIjp7InVzZXJuYW1lIjoiYWRtaW4iLCJwYXNzd29yZCI6IkhhcmJvcjEyMzQ1IiwiYXV0aCI6IllXUnRhVzQ2U0dGeVltOXlNVEl6TkRVPSJ9fX0=" }
            body_metadata = metadata
            body_type = "kubernetes.io/dockerconfigjson"
            body = self.client.V1Secret( 
                api_version = body_api_version,
                kind = body_kind,
                data = body_data,
                metadata = body_metadata, 
                type = body_type
            )
            
            # pprint(body)
            api_response = self.core_v1_api.create_namespaced_secret(namespace,body,_request_timeout=_request_timeout)
            # pprint(api_response)
            return True 
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_cluster_role_binding: %s\n" % str(e))
            return False

    def create_pod_body(self, pod_body):
        containers = [
            {
                "name": pod_body['labels_name'],
                "image": pod_body["image"],
                "ports":[{"containerPort": 8270}],
                "command": [
                    "/usr/bin/AutoStart"
                ],
                "args": [
                    "-D"
                ],
                "resources": pod_body['resources'],
                "imagePullPolicy": "Always",
                "securityContext": {
                    "capabilities": {
                        "add": [
                            "NET_ADMIN",
                            "SYS_TIME"
                        ]
                    },
                    "privileged": True
                }
            }
        ]
        body = self.client.V1Pod()
        spec = self.client.V1PodSpec(containers=containers,dns_policy="Default")
        metadata = self.client.V1ObjectMeta()
        body.api_version = pod_body['api_version']
        body.kind = pod_body['kind']
        metadata.name = pod_body['labels_name']
        metadata.namespace = pod_body['namespace']
        metadata.labels = {
          "k8s-app":  pod_body['labels_name']
        }
        body.metadata = metadata
        body.spec = spec
        return body
    
    def create_namespaced_pod(self,namespace,body):
        namespace = namespace  # str | object name and auth scope, such as for teams and projects

        try:
            api_response = self.core_v1_api.create_namespaced_pod(namespace, body)
            print('create_namespaced_pod %s',api_response)
            return api_response
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_pod: %s\n" % str(e))
    
    def create_deployment_object(self,body):
        name = body.get('metadata').get('name')
        annotations = body.get('metadata').get('annotations')
        image = body.get('spec').get('template').get('spec').get('containers')[0].get('image')
        api_version = body.get('apiVersion')
        kind = body.get('kind')
        replicas = body.get('spec').get('replicas')
        limits = body.get('spec').get('template').get('spec').get('containers')[0].get('resources').get('limits')
        requests = body.get('spec').get('template').get('spec').get('containers')[0].get('resources').get('requests')
        command = body.get('spec').get('template').get('spec').get('containers')[0].get('command')
        image_pull_policy = body.get('spec').get('template').get('spec').get('containers')[0].get('imagePullPolicy')
        privileged = body.get('spec').get('template').get('spec').get('containers')[0].get('securityContext').get('privileged')
        node_selector = body.get('spec').get('template').get('spec').get('node_selector')
        image_pull_secrets = body.get('spec').get('template').get('spec').get('image_pull_secrets')
        security_context = client.V1SecurityContext(privileged=privileged)
        resources_obj = client.V1ResourceRequirements(limits=limits, requests=requests)
        container = client.V1Container(
            name=name,
            image_pull_policy=image_pull_policy,
            security_context=security_context,
            command=command,
            resources=resources_obj,
            image=image)
            # ports=[client.V1ContainerPort(container_port=container_port)])
        # Create and configurate a spec section
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": name},annotations=annotations),
            spec=client.V1PodSpec(containers=[container],node_selector=node_selector,image_pull_secrets=image_pull_secrets))
        # Create the specification of deployment
        spec = client.AppsV1beta1DeploymentSpec(
            replicas=replicas,
            template=template)
        # Instantiate the deployment object
        deployment = client.AppsV1beta1Deployment(
            api_version=api_version,
            kind=kind,
            metadata=client.V1ObjectMeta(name=name,annotations=annotations),
            spec=spec)

        return deployment
    
    def create_deployment(self,namespace,deployment,_request_timeout=(3600,3600)):
        # Create deployement
        api_response=False
        try:
            api_response = self.apps_v1beta1.create_namespaced_deployment(
                body=deployment,
                namespace=namespace,
                _request_timeout=_request_timeout)
            # print(api_response)
            api_response=True
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_deployment: %s\n" % e)
            raise Exception("Exception when calling CoreV1Api->create_deployment: %s\n"%(str(e)))
        return api_response
    
    def create_service_body_dep(self, service_body,_request_timeout):
        body = self.client.V1Service()
        spec = self.client.V1ServiceSpec()
        metadata = self.client.V1ObjectMeta()
        status = self.client.V1ServiceStatus()
        name = service_body.get('metadata').get('name')
        body.api_version = service_body['apiVersion']
        body.kind = service_body['kind']
        spec.ports = service_body.get('spec').get('ports')
        spec.selector = {
            "app": name
        }
        spec.type = service_body.get('spec').get('type')
        metadata.name = name
        metadata.namespace = service_body.get('metadata').get('namespace')
        body.metadata = metadata
        body.spec = spec
        status.loadBalancer = {}
        body.status = status

        namespace=service_body.get('metadata').get('namespace')
        api_response=False
        ports=[]
        for i in range(10):
            try:
                if ports ==[]:
                    api_response = self.core_v1_api.create_namespaced_service(namespace, body,_request_timeout=_request_timeout)
                    # print(api_response)
                    ports=api_response.spec.ports
                    api_response=True
                    print("Exception when calling CoreV1Api->create_namespaced_service times %s ok\n" %(str(i)))
                    break
                else:
                    time.sleep(6)
                    print("Exception when calling CoreV1Api->create_namespaced_service times %s fail\n"%(str(i)))
                    if i == 5:
                        raise Exception("Exception when calling CoreV1Api->create_namespaced_service")
                    continue
            except ApiException as e:
                print("Exception when calling CoreV1Api->create_namespaced_service times %s fail %s\n" % (str(i),
                                                                                                                str(e)))
                if e.status == 409:
                    print("Exception when calling CoreV1Api->create_namespaced_service status conflict "
                                "409 times %s ok\n" % (str(i)))
                    break
                if i == 5:
                    raise Exception("Exception when calling CoreV1Api->create_namespaced_service: %s\n" % e)
                continue

        return api_response,ports
    
    def create_ingress_body(self,ingress_body):
        api_version=ingress_body.get('apiVersion')
        kind=ingress_body.get('kind')
        name = ingress_body.get('metadata').get('name')
        namespace = ingress_body.get('metadata').get('namespace')
        annotations = ingress_body.get('metadata').get('annotations')
        metadata = client.V1ObjectMeta(name=name,namespace=namespace,annotations=annotations)
        host = ingress_body.get('spec').get('rules')[0].get('host')
        service_name=ingress_body.get('spec').get('rules')[0].get('http').get('paths')[0].get('backend').get('serviceName')
        servicePort=ingress_body.get('spec').get('rules')[0].get('http').get('paths')[0].get('backend').get('servicePort')
        backend=client.ExtensionsV1beta1IngressBackend(service_name=service_name,service_port=servicePort)
        paths=client.ExtensionsV1beta1HTTPIngressPath(backend=backend)
        http=client.ExtensionsV1beta1HTTPIngressRuleValue(paths=[paths])
        rules = client.ExtensionsV1beta1IngressRule(host=host,http=http)
        spec = client.ExtensionsV1beta1IngressSpec(rules=[rules])
        body = client.ExtensionsV1beta1Ingress(api_version=api_version,kind=kind,metadata=metadata,spec=spec)
        return body
    
    def create_ingress_body_dep(self, ingress_body,_request_timeout):
        api_response=False
        try:
            namespace=ingress_body.get('metadata').get('namespace')
            body=self.create_ingress_body(ingress_body)
            api_response = self.extensions_v1_beta1_api.create_namespaced_ingress(namespace, body,_request_timeout=_request_timeout)
            # print(api_response)
            api_response = True
        except ApiException as e:
            print("Exception when calling ExtensionsV1beta1Api->create_ingress_body_dep: %s\n" % e)
            raise Exception("Exception when calling ExtensionsV1beta1Api->create_ingress_body_dep: %s\n"%(str(e)))

        return api_response

    def attach_network(self,namespace,network,_request_timeout=(3600,3600)):
        # Create deployement
        api_response=False
        try:
            api_response = self.attach_network_with_http_info(
                apps = self.apps_v1beta1,
                body=network,
                namespace=namespace,
                _request_timeout=_request_timeout)
            # print(api_response)
            api_response=True
        except ApiException as e:
            print("Exception when calling CoreV1Api->attach-network: %s\n" % e)
            raise Exception("Exception when calling CoreV1Api->attach-network: %s\n"%(str(e)))
        return api_response
    
    def attach_network_with_http_info(self,apps, namespace, body, **kwargs):  # noqa: E501
        """create_network  # noqa: E501
        """

        local_var_params = locals()

        all_params = ['namespace', 'body', 'pretty', 'dry_run', 'field_manager']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_namespaced_deployment" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'namespace' is set
        if ('namespace' not in local_var_params or
                local_var_params['namespace'] is None):
            raise ValueError("Missing the required parameter `namespace` when calling `create_namespaced_deployment`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in local_var_params or
                local_var_params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_namespaced_deployment`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'namespace' in local_var_params:
            path_params['namespace'] = local_var_params['namespace']  # noqa: E501

        query_params = []
        if 'pretty' in local_var_params:
            query_params.append(('pretty', local_var_params['pretty']))  # noqa: E501
        if 'dry_run' in local_var_params:
            query_params.append(('dryRun', local_var_params['dry_run']))  # noqa: E501
        if 'field_manager' in local_var_params:
            query_params.append(('fieldManager', local_var_params['field_manager']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        # HTTP header `Accept`
        header_params['Accept'] = apps.api_client.select_header_accept(
            ['application/json', 'application/yaml', 'application/vnd.kubernetes.protobuf'])  # noqa: E501

        # Authentication setting
        auth_settings = ['BearerToken']  # noqa: E501

        return apps.api_client.call_api(
            '/apis/k8s.cni.cncf.io/v1/namespaces/{namespace}/network-attachment-definitions', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AppsV1beta1Deployment',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats
            )
        
    def delete_deployment(self,dep_body_dict,_request_timeout):
        # del deployement
        namespace = dep_body_dict.get('metadata').get('namespace')
        name = dep_body_dict.get('metadata').get('name')
        api_response=False
        try:
            body = client.V1DeleteOptions(propagation_policy='Background')
            api_response = self.apps_v1beta1.delete_namespaced_deployment(name=name,namespace=namespace,body=body,
                                                                        _request_timeout=_request_timeout)
            # print(api_response)
            api_response = True
        except ApiException as e:
            print("Exception when calling AppsV1Api->delete_namespaced_deployment: %s\n" % e)
        # print("Deployment created. status='%s'" % str(api_response.status))
        return api_response

    def delete_namespaced_deployment(self,name,namespace):
        try:
            api_response = self.apps_v1_api.delete_namespaced_deployment(name, namespace)
            print('delete_namespaced_deployment %s', api_response)
        except ApiException as e:
            print("Exception when calling AppsV1Api->delete_namespaced_deployment: %s\n" % str(e))
    
    def delete_service_body_dep(self, service_body,_request_timeout):
        api_response=False
        namespace = service_body.get('metadata').get('namespace')
        name = service_body.get('metadata').get('name')
        try:
            api_response = self.core_v1_api.delete_namespaced_service(name, namespace,_request_timeout=_request_timeout)
            # print(api_response)
            api_response=True
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_service: %s\n" % e)
        return api_response
    
    def list_nodes(self):
        try:
            api_response = self.core_v1_api.list_node()
            # pprint(api_response)
            return api_response
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_node: %s\n" % e)
            return False
    
    def delete_network(self,net_body_dict,_request_timeout):
        namespace = net_body_dict.get('metadata').get('namespace')
        name = net_body_dict.get('metadata').get('name')
        api_response=False
        try:
            body = client.V1DeleteOptions(propagation_policy='Background')
            api_response = self.delete_namespaced_network_with_http_info(
                apps = self.apps_v1beta1,
                name=name,
                namespace=namespace,
                body = body,
                _request_timeout=_request_timeout
                )
            # print(api_response)
            api_response = True
        except ApiException as e:
            print("Exception when calling AppsV1Api->delete_namespaced_deployment: %s\n" % e)
        # print("Deployment created. status='%s'" % str(api_response.status))
        return api_response

    def delete_namespaced_network_with_http_info(self, apps, name, namespace, **kwargs): 
        local_var_params = locals()

        all_params = ['name', 'namespace', 'pretty', 'dry_run', 'grace_period_seconds', 'orphan_dependents', 'propagation_policy', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_namespaced_deployment" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'name' is set
        if ('name' not in local_var_params or
                local_var_params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `delete_namespaced_deployment`")  # noqa: E501
        # verify the required parameter 'namespace' is set
        if ('namespace' not in local_var_params or
                local_var_params['namespace'] is None):
            raise ValueError("Missing the required parameter `namespace` when calling `delete_namespaced_deployment`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'name' in local_var_params:
            path_params['name'] = local_var_params['name']  # noqa: E501
        if 'namespace' in local_var_params:
            path_params['namespace'] = local_var_params['namespace']  # noqa: E501

        query_params = []
        if 'pretty' in local_var_params:
            query_params.append(('pretty', local_var_params['pretty']))  # noqa: E501
        if 'dry_run' in local_var_params:
            query_params.append(('dryRun', local_var_params['dry_run']))  # noqa: E501
        if 'grace_period_seconds' in local_var_params:
            query_params.append(('gracePeriodSeconds', local_var_params['grace_period_seconds']))  # noqa: E501
        if 'orphan_dependents' in local_var_params:
            query_params.append(('orphanDependents', local_var_params['orphan_dependents']))  # noqa: E501
        if 'propagation_policy' in local_var_params:
            query_params.append(('propagationPolicy', local_var_params['propagation_policy']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        # HTTP header `Accept`
        header_params['Accept'] = apps.api_client.select_header_accept(
            ['application/json', 'application/yaml', 'application/vnd.kubernetes.protobuf'])  # noqa: E501

        # Authentication setting
        auth_settings = ['BearerToken']  # noqa: E501

        return apps.api_client.call_api(
            '/apis/k8s.cni.cncf.io/v1/namespaces/{namespace}/network-attachment-definitions/{name}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='V1Status',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_namespaced_deployment(self, namespace):
        try:
            api_response = self.apps_v1_api.list_namespaced_deployment(namespace)
            pprint(api_response)
            return api_response
        except ApiException as e:
            print("Exception when calling APPSV1Api->list_namespaced_deployment: %s\n" % e)
            return False

