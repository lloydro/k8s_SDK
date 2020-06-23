#!/usr/bin/env python
# -*- coding:utf8 -*-
from __future__ import absolute_import
from __future__ import print_function
import uuid
from KubeApi.utils.kubeExec import KubeExec
import time
import json
import subprocess
import os
import platform



class KubeTask(object):
    def __init__(self):
        pass

    def create_namespace(self, namespace,config_file=None,context=None,_request_timeout=(3600,3600)):
        conn = KubeExec(config_file=config_file,context=context)
        status = conn.create_namespace(namespace,_request_timeout=_request_timeout)
        return status

    def create_service_account(self, namespace,config_file=None,context=None,_request_timeout=(3600,3600)):
        conn = KubeExec(config_file=config_file,context=context)
        status = conn.create_service_account(namespace,_request_timeout=_request_timeout)
        return status

    def create_role(self, namespace,config_file=None,context=None,_request_timeout=(3600,3600)):
        conn = KubeExec(config_file=config_file,context=context)
        status = conn.create_role(namespace,_request_timeout=_request_timeout)
        return status

    def create_role_binding(self, namespace,config_file=None,context=None,_request_timeout=(3600,3600)):
        conn = KubeExec(config_file=config_file,context=context)
        status = conn.create_role_binding(namespace,_request_timeout=_request_timeout)
        return status
    
    def create_cluster_role(self, namespace,config_file=None,context=None,_request_timeout=(3600,3600)):
        conn = KubeExec(config_file=config_file,context=context)
        status = conn.create_cluster_role(namespace,_request_timeout=_request_timeout)
        return status

    def create_cluster_role_binding(self, namespace,config_file=None,context=None,_request_timeout=(3600,3600)):
        conn = KubeExec(config_file=config_file,context=context)
        status = conn.create_cluster_role_binding(namespace,_request_timeout=_request_timeout)
        return status
    
    def create_secret(self, namespace,config_file=None,context=None,_request_timeout=(3600,3600)):
        conn = KubeExec(config_file=config_file,context=context)
        status = conn.create_secret(namespace,_request_timeout=_request_timeout)
        return status

    def create_container_with_deploy(self, dep_body_dict,config_file=None,context=None,_request_timeout=(3600,3600)):
        conn = KubeExec(config_file=config_file,context=context)
        if isinstance(dep_body_dict,str):
            dep_body_dict = json.loads(dep_body_dict)
        namespace = dep_body_dict.get('metadata').get('namespace')
        deployment = conn.create_deployment_object(dep_body_dict)
        status = conn.create_deployment(namespace,deployment,_request_timeout=_request_timeout)

        return status

    def create_service_deploy(self, service_body,config_file=None,context=None,_request_timeout=(3600,3600)):
        if isinstance(service_body,str):
            service_body = json.loads(service_body)
        conn = KubeExec(config_file=config_file, context=context)
        status,ports = conn.create_service_body_dep(service_body,_request_timeout=_request_timeout)
        return status,ports
    
    def create_ing_deploy(self, ing_body,config_file=None,context=None,_request_timeout=(3600,3600)):
        if isinstance(ing_body,str):
            ing_body = json.loads(ing_body)
        conn = KubeExec(config_file=config_file, context=context)
        status = conn.create_ingress_body_dep(ing_body,_request_timeout=_request_timeout)
        return status

    def delete_container_with_deploy(self, dep_body_dict,config_file=None,context=None,_request_timeout=(3600,3600)):
        conn = KubeExec(config_file=config_file,context=context)
        if isinstance(dep_body_dict,str):
            dep_body_dict = json.loads(dep_body_dict)
        status = conn.delete_deployment(dep_body_dict,_request_timeout=_request_timeout)
        return status

    def delete_service_deploy(self, service_body,config_file=None,context=None,_request_timeout=(3600,3600)):
        if isinstance(service_body,str):
            service_body = json.loads(service_body)
        conn = KubeExec(config_file=config_file, context=context)
        status = conn.delete_service_body_dep(service_body,_request_timeout=_request_timeout)
        return status

    def delete_network(self,net_body_dict,config_file=None,context=None,_request_timeout=(3600,3600)):
        conn = KubeExec(config_file=config_file,context=context)
        if isinstance(net_body_dict,str):
            net_body_dict = json.loads(net_body_dict)
        status = conn.delete_network(net_body_dict,_request_timeout=_request_timeout)
        return status

    def attach_network(self, net_body_dic,config_file=None,context=None,_request_timeout=(3600,3600)):
        conn = KubeExec(config_file=config_file,context=context)
        if isinstance(net_body_dic,str):
            net_body_dic = json.loads(net_body_dic)
        namespace = net_body_dic.get('metadata').get('namespace')
        status = conn.attach_network(namespace,net_body_dic,_request_timeout=_request_timeout)
        return status

    def list_nodes(self):
        conn = KubeExec()
        status = conn.list_nodes()
        return status
        
    def list_namespaced_deployment(self, namespace):
        conn = KubeExec()
        status = conn.list_namespaced_deployment(namespace)
        return status
    
    def read_node(self,name):
        conn = KubeExec()
        status = conn.read_node(name)
        return status
    
    def read_node_status(self,name):
        conn = KubeExec()
        status = conn.read_node(name)
        return status
    
    def get_node_resource(self,name):
        conn = KubeExec()
        status = conn.get_node_resource(name)
        return status
    
    def list_pod_for_all_namespaces(self):
        conn = KubeExec()
        status = conn.list_pod_for_all_namespaces()
        return status
    
    def list_namespaced_pod(self,namespace):
        conn = KubeExec()
        status = conn.list_namespaced_pod(namespace)
        return status
