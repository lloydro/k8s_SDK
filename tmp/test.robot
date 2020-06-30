*** Setting ***
Library    Remote    http://172.29.46.205:39186     ${600}     ${600}     ${600}     WITH NAME  remote01
Library    Collections 
Library    json
Library     DateTime
Library           String

Suite Setup    Global Startup 
Suite Teardown    Global End
*** Variables ***
@{list_prog}=       fe.core.ptm.sw


*** Keyword ***   
END_MONITOR
    [Arguments]    ${pid_list}    ${remote}=remote01    ${sleep_time}=3s
    Log    SLEEP一段时间
    Sleep    ${sleep_time}
    Log    杀死监控进程
    : FOR    ${PID}    IN    @{pid_list}
    \    Log    ${PID}
    \    ${result}=    Run Keyword    ${remote}.Remote Shell Cmd    cmd=kill -9 ${PID}
    Log    获取监控信息时间戳
    ${timelog}    Run Keyword    ${remote}.Remote Shell Cmd Get Output    cmd=cat /monitorLog.log | grep publish | grep -v grep | awk '{print $1}'
    Log    判断时间戳不未空
    Should Not Be Empty    ${timelog}
START_MONITOR
    [Arguments]    ${db_name}    ${key}    ${remote}=remote01    ${sleep_time}=1s
    Log    SLEEP一段时间
    Sleep    ${sleep_time}
    LOG    清空monitorLog.log内容
    ${result}=    Run Keyword    ${remote}.Remote Shell Cmd    cmd=cat /dev/null >/monitorLog.log
    LOG    下发monitor监控命令
    ${result}=    Run Keyword    ${remote}.Remote Shell Cmd    cmd=redis-cli -s /tmp/redis/${db_name} MONITOR *${key}* >>/monitorLog.log &
    Log    获取监控进程信息
    ${PID}    Run Keyword    ${remote}.Remote Shell Cmd Get Output    ps -ef | grep ".sock MONITOR" | grep -v grep | awk '{print $2}'
    Log    获取monitor监控pid列表
    ${pid_list}    split string    ${PID}    \n
    [Return]    ${pid_list}

Global Startup
    [Arguments]    ${remote_select}=remote01
    ${global_start_time}=    get_current_date
    Set Global Variable    ${global_start_time}    ${global_start_time}
    log     ${global_start_time}   warn
    # Now Restart Mom
    Run Keyword     ${remote_select}.DEL ALL CORES
    
    Start Process     ${remote_select}
    
Global End
    [Arguments]    ${remote_select}=remote01
    End Process    ${remote_select}
    
    #Coverage   
    ${global_end_time}=    get_current_date
    Set Global Variable    ${global_end_time}    ${global_end_time}
    ${g_inter_time}=     Subtract Date From Date         ${global_end_time}     ${global_start_time}
    log     global ${g_inter_time}     warn
    
Now Restart Mom
    [Arguments]    ${remote_select}=remote01
    Run Keyword     ${remote_select}.Restart Mom     ${6}    
    log   'restart mom ...'   warn
    
Part Startup 
    [Arguments]    ${status}=${False}    ${cmd}=[]    ${remote_select}=remote01
    ${p_start_time}=    get_current_date 
    Set Global Variable    ${p_start_time}    ${p_start_time}
    Run Keyword    ${remote_select}.Remote Setup Children Cap SET    ${cmd}
    #Now Restart Mom
    Run Keyword     ${remote_select}.Rg Mom Finish
    Run Keyword And Return If   ${status}==${False}    log   'not excute Startup Process'   
    Start Process        ${remote_select}
    
Part End
    [Arguments]    ${status}=${False}     ${cmd}=[]    ${remote_select}=remote01  
    End Process    ${remote_select}
    Run Keyword    ${remote_select}.ASSERT PROCESS NOT TRUE
    Run Keyword    ${remote_select}.Remote TearDwon Children Cap SET     ${cmd}
    Run Keyword And Return If   ${status}==${False}    log   'not excute End Process' 
    #Coverage  
    ${p_end_time}=    get_current_date 
    Set Global Variable    ${p_end_time}    ${p_end_time}
    ${p_inter_time}=     Subtract Date From Date         ${p_end_time}     ${p_start_time}
    log     part ${p_inter_time}      warn

Start Process
    [Arguments]    ${remote_select}=remote01
        :FOR    ${proc}    IN    @{list_prog}
    \     Run Keyword    ${remote_select}.Remote Shell Cmd    ${proc} & 
    Sleep    5s
    log   'Excute Startup Process'   warn
    
End Process
    [Arguments]    ${remote_select}=remote01
    :FOR    ${proc}    IN    @{list_prog}
    \    Run Keyword    ${remote_select}.Kill Process    ${proc}    
    Sleep    0.5s
    log   'Excute End Process'     warn
    
Coverage
    [Arguments]    ${remote_select}=remote01
    ${result}=Run Keyword     ${remote_select}.Coverage Statistics
    log         ${result}       warn
    
*** Test Cases ***
RG-BRIDGE-SDP-PORT-ZJ-GN-0520
    [Documentation]    测试用例名称:配置风暴控制-单播
    ...    测试描述：配置风暴控制-单播
    ...    测试步骤:1.输入：端口风暴控制配置-单播
    ...    输入事件1：端口风暴控制配置；数量：1
    ...    2.预期输出：fp服务输出风暴控制配置
    ...    输出事件1：fp服务输出风暴控制配置；数量：1
    [Setup]    Part Startup    True    ["fe.cap.sw &", "ce.cap.sw &", "app_df &", "rg_cap_tran &", "ce.tran.cap.sw &", "rg_cap &", "sleep 2", "ce.en.l3tb.sw &", "/usr/bin/StartSbin.sh", "sleep 6"]
   LOG    step 0:30槽位MODID添加    
    ${result}=     remote01.RG MOM PDEL   db_name=ASIC_DB    class_tree_obj={"namespace": "s__intf__sdp_ddm", "ins_name": "anonymity", "msg_name": "evt_mod_alloc", "repeated": false, "attrs": [{"namespace": "s__intf__sdp_ddm", "ins_name": "index", "msg_name": "mod_alloc_index", "repeated": false, "attrs": [{"basic_msg_ins_level": "s__intf__sdp_ddm.anonymity.index", "basic_msg_level": "s__intf__sdp_ddm.evt_mod_alloc.mod_alloc_index", "value": "", "basic_msg": "INT32", "ins_name": "devid", "namespace": "s__intf__sdp_ddm", "repeated": false}, {"basic_msg_ins_level": "s__intf__sdp_ddm.anonymity.index", "basic_msg_level": "s__intf__sdp_ddm.evt_mod_alloc.mod_alloc_index", "value": "", "basic_msg": "INT32", "ins_name": "slotid", "namespace": "s__intf__sdp_ddm", "repeated": false}, {"basic_msg_ins_level": "s__intf__sdp_ddm.anonymity.index", "basic_msg_level": "s__intf__sdp_ddm.evt_mod_alloc.mod_alloc_index", "value": "", "basic_msg": "INT32", "ins_name": "sslotid", "namespace": "s__intf__sdp_ddm", "repeated": false}, {"basic_msg_ins_level": "s__intf__sdp_ddm.anonymity.index", "basic_msg_level": "s__intf__sdp_ddm.evt_mod_alloc.mod_alloc_index", "value": "", "basic_msg": "INT32", "ins_name": "unit", "namespace": "s__intf__sdp_ddm", "repeated": false}]}, {"basic_msg_ins_level": "s__intf__sdp_ddm.anonymity", "ins_name": "modid", "value": "258", "basic_msg": "INT32", "basic_msg_level": "s__intf__sdp_ddm.evt_mod_alloc", "namespace": "s__intf__sdp_ddm", "repeated": false}, {"basic_msg_ins_level": "s__intf__sdp_ddm.anonymity", "ins_name": "node_type", "value": "p__dev__dev_dp.DM_TYPE_MB", "basic_msg": "p__dev__dev_dp:.p_dev.dm_node_type_e", "basic_msg_level": "s__intf__sdp_ddm.evt_mod_alloc", "namespace": "s__intf__sdp_ddm", "repeated": false}, {"basic_msg_ins_level": "s__intf__sdp_ddm.anonymity", "ins_name": "idnum_per_unit", "value": "1", "basic_msg": "UINT32", "basic_msg_level": "s__intf__sdp_ddm.evt_mod_alloc", "namespace": "s__intf__sdp_ddm", "repeated": false}]}    delay=100    level=0    
   LOG    result: ${result}    
    [Teardown]    Part End    True    ["cd /home/x86rgos/;sh run_12.x_mom.sh restart", "sleep 3"]

