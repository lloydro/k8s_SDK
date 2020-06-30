#!/usr/bin/python
# -*- coding:utf8 -*-
from requests import request
import json
from requests.auth import HTTPBasicAuth
import platform
import os
import sys
import subprocess
import paramiko
from requests_toolbelt import MultipartEncoder
import requests
import time

def update_hosts(content):
    already_content = False
    sysstr = platform.system()
    if sysstr == "Windows":
        print("Call Windows tasks")
        with open(r'C:\WINDOWS\system32\drivers\etc\hosts', 'r', encoding='UTF-8') as wf:
            lines = wf.readlines()
            for line in lines:
                line = line.strip()
                if content == line:
                    already_content = True
        if not already_content:
            with open(r'C:\WINDOWS\system32\drivers\etc\hosts', "a+") as wf:
                wf.write(content + "\n")

    elif sysstr == "Linux":
        print("Call Linux tasks")
        with open('/etc/hosts', "r") as wf:
            lines = wf.readlines()
            for line in lines:
                line = line.strip()
                if content == line:
                    already_content = True
        if not already_content:
            with open('/etc/hosts', "a+") as wf:
                wf.write(content + "\n")
    else:
        print("Other System tasks: %s" % sysstr)


def delete_hosts(content):
    sysstr = platform.system()
    hosts_url = '/etc/hosts'
    if sysstr == "Windows":
        print("Call Windows tasks")
        hosts_url = r'C:\WINDOWS\system32\drivers\etc\hosts'
    elif sysstr == "Linux":
        print("Call Linux tasks")
        hosts_url = '/etc/hosts'
    cmd = 'sed -i "/%s/d" %s' % (content, hosts_url)
    result = cmd_shell(cmd)
    print(str(result))


def update_ip(content, url):
    import re
    already_content = False
    file_data = ''
    content = content + '     ${600}'
    with open(url, 'r', encoding='UTF-8') as wf:
        lines = wf.readlines()
        for line in lines:
            pattern = re.compile(
                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
            pat_list = pattern.findall(line)
            if not already_content:
                line = re.sub(pattern, content, line)
            file_data += line
            if pat_list:
                already_content = True
    with open(url, "w", encoding="utf-8") as f:
        f.write(file_data)


def cmd_shell(cmd):
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=7200).decode().strip()
        return result
    except Exception as e:
        print(e)


def init_env(ssh_ip, ssh_port, conan_argv, dev, project):
    connect = 0
    while connect == 0:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ssh_ip, ssh_port, 'root', '123456', timeout=86400)
        except Exception:
            connect == 0
        else:
            connect = 1
            print("connect success!")
        # 安装conan包
    if conan_argv != 'none':
        stdin, stdout, stderr = client.exec_command('cd / && ls -l | grep -o "work.*" | xargs rm -rf')
        for i in stderr.readlines():
            print(i)
        for i in stdout.readlines():
            print(i)
        stdin, stdout, stderr = client.exec_command('find / -name *.gcno | xargs rm -rf')
        for i in stderr.readlines():
            print(i)
        for i in stdout.readlines():
            print(i)
        if 'compile_daily' not in conan_argv:
            stdin, stdout, stderr = client.exec_command(
                'cd /home/x86rgos && source x86-env-setup && bash -x /home/x86rgos/conan.sh %s' % conan_argv.replace(
                    ';', ' '))
            for i in stderr.readlines():
                print(i)
            for i in stdout.readlines():
                print(i)

        stdin, stdout, stderr = client.exec_command('/usr/bin/RfRemote restart')
        for i in stderr.readlines():
            print(i)
        for i in stdout.readlines():
            print(i)
        # 切换设备型号
    stdin, stdout, stderr = client.exec_command(
        "cd /home/x86rgos && source x86-env-setup && bash  /home/change_dev.sh %s %s" % (dev, project))
    for i in stderr.readlines():
        print(i)
    for i in stdout.readlines():
        print(i)
        # 重启能力进程和数据库
    stdin, stdout, stderr = client.exec_command('/home/x86rgos/normal_init.sh')
    print(stdout.readline())


# 生成info文件
def gen_info(ssh_ip, ssh_port, com, cc_port):
    print('生成info文件')
    connect = 0
    while connect == 0:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ssh_ip, ssh_port, 'root', '123456', timeout=12000)
        except Exception:
            connect == 0
        else:
            connect = 1
            print("connect success!")
    stdin, stdout, stderr = client.exec_command(
        "cd /home/x86rgos && source x86-env-setup && bash /home/gcov.sh %s %s" % (com, cc_port))
    for i in stderr.readlines():
        print(i)
    for i in stdout.readlines():
        print(i)


def check_domain(domain, port=80):
    status = False
    twice = 1
    fail_times = 1
    for t_n in range(180):
        time.sleep(10)
        try:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
            header = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'User-Agent': user_agent,
                'Connection': 'close'
            }
            url = 'http://' + domain + ':%s' % (str(port))
            requests.adapters.DEFAULT_RETRIES = 10
            s = requests.session()
            s.keep_alive = False
            s.headers = header
            s.timeout = 10
            result = s.get(url)
            status_code = result.status_code
            s.close()
            if status_code == 501:
                twice = twice + 1
                print('connect to container %s domain %s ok twice %s' % (str(port), domain, str(twice)))
                if twice == 4:
                    status = True
                    break
            else:
                status = False
                print('connect to container %s domain %s' % (str(port), domain))
                continue
        except Exception as e:
            fail_times = fail_times + 1
            if fail_times >= 100:
                raise Exception(
                    'can not connect to container doamin %s port %s, please check port' % (domain, str(port)))
            else:
                print('connect to container %s %s domain %s' % (str(e), str(port), domain))
                status = False
                continue
    if status:
        time.sleep(5)
        print('connect to container domain %s %s OK' % (str(port), domain))
        return True
    else:
        raise Exception('can not connect to container doamin %s port %s, please check port' % (domain, str(port)))



def check_port(ip, port=8270):
    import socket
    status =False
    times = 1
    for t_n in range(180):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(30)
        try:
            s.connect((ip, port))
            status = True
            s.close()
            times = times + 1
            if times == 4:
                break
            else:
                continue
        except Exception as e:
            print('connect to container %s %s ip %s'%(str(port),str(e), ip))
            status = False
    if status:
        time.sleep(5)
        print('connect to container %s OK'%(str(port)))
        return True
    else:
        raise Exception('can not connect to container port %s, please check port'%(str(port)))


def remote_shell_cmd_get_output(cmd, timeout=20):
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT,
                                             timeout=timeout).decode().strip()
        return result
    except Exception as e:
        # out_bytes = e.output
        out_bytes = str(e)
        raise Exception('%s' % (out_bytes))

def rcmd(host, password,cmd, port=22, username='root', timeout=7200):
    for i in range(3):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=username, password=password, port=port, timeout=timeout,
                        banner_timeout=timeout)
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
            data = stdout.read().decode('utf8')
            error = stderr.read()
            print('rcmd cmd:%s'%(cmd))
            ssh.close()
            return data
        except Exception as e:
            raise Exception('host %s rcmd  %s error %s ' % (host, cmd, str(e)))

def remote_shell(domain,exe_data,password='123456',ssh_port=22):
    for cmd in exe_data['cmd_list']:
        cmd_report = rcmd(domain, password, cmd, port=ssh_port, username='root', timeout=7200)
        print('cmd:%s' % (cmd))
        print('cmd_report %s' % (cmd_report))

def run(file_name, image, dev, project, conan_argv, com, cc_port):
    from KubeApi.app import KubeClient
    excute_status = 'True'
    sysstr = platform.system()
    if sysstr == "Windows":
        file_name = r'%s' % (file_name)
    createData = [{                      # 构造参数
    "image" : image,
    "command" : '/usr/bin/AutoStart',
    "cpu" : 350,
    "memory" : 500,
    "ephemeral_storage" : 8,
    "ports": [22,3306,4200,8270]
}]
    uid = 'wangyongcheng'
    kubeClient = KubeClient(uid)     # 初始化
    content = kubeClient.handle('deployment','CREATE',createData)

    for pod_name,body in content['datas']['deps'].items():
        domain = body['host_ip']
        port = body['rf_port']
        ssh_port = body['ssh_port']
        name = body['name']
        print('创建容器成功 %s'%(pod_name))
        try:
            if excute_status == 'True':
                exe_data = {
                    "cmd_list": ['cd /home/x86rgos && source x86-env-setup && bash /home/x86rgos/conan.sh %s' % (
                        conan_argv.replace(';', ' ')), 'bash /home/change_dev.sh %s %s' % (dev, project.split('_')[-1]),
                                 'bash /home/x86rgos/normal_init.sh'],
                    "pod_name": name,
                    "namespace": "ceshi"
                }
                print("exe exe_data %s" % (exe_data))
                print("check_port %s %s %s doing"%(domain,port,file_name))
                check_port(domain, port=ssh_port)
                print("check_port %s %s %s done"%(domain,port,file_name))
                print('remote_shell doing %s  %s'%(exe_data,file_name))
                remote_shell(domain, exe_data, password='123456',ssh_port=ssh_port)
                print('remote_shell done %s  %s'%(exe_data,file_name))
                update_ip('http://' + domain + ':' + str(port), file_name)
                case_name = file_name.split('/', file_name.count("/"))[-1][:-6]
                filename_with_dev = file_name.replace(case_name, dev + '_' + case_name)
                # print('remote_shell_cmd_get_output %s'%('cp %s %s' % (file_name, filename_with_dev)))
                # output = remote_shell_cmd_get_output('cp %s %s' % (file_name, filename_with_dev), timeout=5400)
                # print(str(output))
                check_port(domain, port=port)
                r_cmd='robot --loglevel DEBUG -T -l %s_%s_log.html -o %s_%s_output.xml -r %s_%s_report.html  %s' % (
                dev, case_name, dev, case_name, dev, case_name, filename_with_dev)
                print('用例%s r_cmd %s doing'%(case_name,r_cmd))
                output = subprocess.call(r_cmd, shell=True,timeout=5400)
                print('用例%s r_cmd %s done'%(case_name,r_cmd))
                print('用例执行结果:%s'%(str(output)))

            if conan_argv != 'none':
                print('用例%s 覆盖率统计开始'%(case_name))
                gen_info(body["host_ip"], body["ssh_port"], com, cc_port)
                print('用例%s 覆盖率统计结束'%(case_name))

            if name != []:
                data = [
                     {
                           "name" : name

                     },
                ]
                result = kubeClient.handle('deployment','DELETE',data)
                if result['status'] is True:
                    print('用例%s 删除容器成功 %s'%(case_name,data))
                else:
                    print('用例%s 删除容器失败 %s'%(case_name,data))
        except Exception as e:
            if name != []:
                data = [
                    {
                        "name": name

                    },
                ]
                result = kubeClient.handle('deployment', 'DELETE', data)
                if result['status'] is True:
                    print('用例%s 删除容器成功 %s' % (case_name, data))
                else:
                    print('用例%s 删除容器失败 %s' % (case_name, data))


run('E:\\tests\\SDK\\k8s_SDK\\tmp\\test.robot', 'docker-hub.ruijie.work/base_project/robotframework-branch_12.5pl1:latest',   'dev',  'project' , 'conan_argv', 'com','cc_port')