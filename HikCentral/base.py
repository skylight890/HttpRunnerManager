# encoding: utf-8

# -*- coding: utf-8 -*-

"""==================================================================
Copyright(c) 2016-2017 Hangzhou Hikvision Digital Technology Co.,Ltd
文件名称:  Base.py
简要描述： 通讯基础模块，提供通信类的创建、测试类的封装
           编写测试用例时需要导入Base模块
作    者： Qiu Jiangping
完成日期:  2017-5-11
修订说明:
=================================================================="""

import ctypes
import time, traceback
from .logger import LogRecord
from .utils import *
# from PostgreSqlInterface import *

g_logRecord = LogRecord()

# 通信类
class Connect:
    """============================================================================================
    函数名称: __init__
    功能描述: 初始化, 加载lib目录下的dll文件
    参数列表: 无
    返回结果: 无
    ==============================================================================================="""

    def __init__(self):
        # lib_dir = g_rootPath + "\\Lib"
        # os.chdir(lib_dir)
        self.dll = ctypes.CDLL(".\\ISAPITest.dll")
        # os.chdir(g_rootPath)
        self.dll.Init()
        self.login_id = 0
        # 统计每条协议耗时
        self.elapsed = 0

    """============================================================================================
    函数名称: __del__
    功能描述: 反初始化
    参数列表: 无
    返回结果: 无
    ==============================================================================================="""

    def __del__(self):
        pass  # self.dll.Uninit()

    """============================================================================================
    函数名称: login
    功能描述: 登陆VSM服务器
    参数列表: ip——服务器ip地址
              port——服务器端口
              user——用户名
              pwd——用户密码
              clientType—客户端类型, 0: WebClient, 1: PCClient, 2: MobileClient
              httpType-http类型, 0: http, 1:https, 默认为http
    返回结果: 返回登陆句柄, -1为无效值, 其他正直有效     
    ==============================================================================================="""

    def login(self, ip, port, user, pwd, clientType=0, httpType=0):
        self.login_id = self.dll.Login(ip, port, user, pwd, clientType, 'http' if httpType == 0 else 'https');
        if (self.login_id != -1):
            error_info = '=============== [Login Success] ===============\r'
            g_logRecord.log_info(error_info)
        else:
            error_info = '=============== [Login Fail] ip: %s, port: %s, username: %s, pwd: %s, client type: %s ===============\r' % (
            ip, str(port), user, pwd, str(clientType))
            g_logRecord.log_error(error_info)

        return self.login_id

    """============================================================================================
    函数名称: logout
    功能描述: 登出系统接口
    参数列表: 无
    返回结果: 无
    ==============================================================================================="""

    def logout(self):  # 退出登录
        self.dll.LogOut(self.login_id)

        # 记录日志
        g_logRecord.log_info('=============== [Logout] ===============\r')
        print('=============== [Logout] ===============\r')

    """============================================================================================
    函数名称: 通过login_id获取SessionID
    功能描述: 获取SID
    返回结果: SID    
    ==============================================================================================="""

    def getSessionID(self):
        sid = self.dll.GetSessionID(self.login_id)
        return self.dll.GetSessionID(self.login_id)

    """============================================================================================
    函数名称: Encrypt
    功能描述: AES加密方式(用于增加设备时输入密码加密)
    参数列表: pwd——需要加密的密码
              loginPwd——系统登录密码
    返回结果: 返回加密后的密码
    ==============================================================================================="""

    def Encrypt(self, pwd, loginPwd="Abc12345"):
        self.PW = self.dll.AESEncrypt(self.login_id, pwd, loginPwd)
        self.PW = ctypes.string_at(self.PW, -1)
        return self.PW

    """============================================================================================
    函数名称: RSA_Encrypt
    功能描述: RSA加密方式
    参数列表: pwd——需要加密的密码
    返回结果: 返回加密后的密码
    ==============================================================================================="""

    def RSA_Encrypt(self, pwd="Abc12345"):
        self.RSA_PW = self.dll.RSAEncrypt(self.login_id, pwd)
        self.RSA_PW = ctypes.string_at(self.RSA_PW, -1)
        return self.RSA_PW

    """============================================================================================
    函数名称: cmd
    功能描述: 系统交互命令接口
    参数列表: url——请求url路径；
              method——请求方法：get、post、put、delete
              query_param——请求Query;
              need_sid——是否需要SID(session id), 1：需要 0：不需要
              content——请求内容;
              send_overtime——发送超时时间, 默认30s;
              recv_overtime——接收超时时间, 默认30s;
    返回结果: 期望Response数据     
    ==============================================================================================="""

    def cmd(self, url, method, query_param, need_sid, content, send_overtime=30000, recv_overtime=30000):
        # 计时
        self.elapsed = 0
        start_time = time.time()
        try:
            ret = self.dll.SendEx(self.login_id, method, url, content, query_param, need_sid,
                                  "application/xml; charset=\"UTF-8\"", send_overtime, recv_overtime)
            self.elapsed = self.get_format_elapse(float('{0:.3} '.format((time.time() - start_time))))
            # ret = self.dll.Send(self.login_id, method, url, content, query_param)
            ret = ctypes.string_at(ret, -1).decode('utf-8')
        except:
            traceback.print_exc()
            g_logRecord.writeText2Log(
                'Except: dll.SendEx(\rlogin_id: %s\rmethod: %s\rurl: %s\rcontent: %s\rquery_param: %s\rneed_sid: %s\rsend_time_out:%s\rRecv_time_out:%s)'
                % (str(self.login_id), method, url, content, query_param, str(need_sid), str(send_overtime),
                   str(recv_overtime)), 2)
        return ret

    def get_format_elapse(self, elapse):
        integer = int(elapse)
        decimal = elapse - integer
        h = integer / 3600
        sUp_h = integer - 3600 * h
        m = sUp_h / 60
        s = sUp_h - 60 * m
        time_list = map(lambda x: "0%d" % x if 0 <= x < 10 else str(x), [h, m, s])
        ms = '%.2f' % decimal
        ms = ms[1:]
        return ":".join(time_list) + ms


# 测试类
class TestGroup:
    """============================================================================================
    函数名称: __init__
    功能描述: 初始化
    参数列表: serverType——登录服务器类型；
    返回结果: 无
    ==============================================================================================="""

    def __init__(self, serverType='VSM_Server'):
        # 获取登录对应服务器的参数
        (self.ip, self.port, self.username, self.loginPw, self.clientType) = g_login_params_dict[serverType]
        # 定义通讯对象
        self.conn = Connect()
        # 定义测试结果
        (self.bResult, self.failReason_list) = (True, [])

    """============================================================================================
    函数名称: __del__
    功能描述: 反初始化
    参数列表: 无
    返回结果: 无
    ==============================================================================================="""

    def __del__(self):
        pass

    """============================================================================================
    函数名称: loginVsm
    功能描述: 登录VSM服务器
    参数列表: 无
    返回结果: 无
    ==============================================================================================="""

    def loginVsm(self):
        return self.conn.login(self.ip, self.port, self.username, self.loginPw, self.clientType)

    """============================================================================================
    函数名称: logoutVsm
    功能描述: 登出VSM服务器
    参数列表: 无
    返回结果: 无
    ==============================================================================================="""

    def logoutVsm(self):
        return self.conn.logout()

    """============================================================================================
    函数名称: getSessionID
    功能描述: 获取sessionID
    参数列表: 无
    返回结果: 无
    ==============================================================================================="""

    def getSessionID(self):
        return self.conn.getSessionID()

    """============================================================================================
    函数名称: initTestResult
    功能描述: 初始化测试结果详情
    参数列表: 无
    返回结果: 无
    ==============================================================================================="""

    def initTestResult(self):
        (self.bResult, self.failReason_list) = (True, [])

    """============================================================================================
    函数名称: getTestResult
    功能描述: 获取测试结果详情
    参数列表: 无
    返回结果: 无
    ==============================================================================================="""

    def getTestResult(self):
        return (self.bResult, ''.join(self.failReason_list))

    """============================================================================================
    函数名称: recordTestResult
    功能描述: 记录错误详情
    参数列表: bRet——Response比较结果;strMsg——Response比较结果详情
    返回结果: 无
    ==============================================================================================="""

    def recordTestResult(self, bRet, strMsg):
        if bRet == False:
            self.bResult = False
            self.failReason_list.append(strMsg)
        else:
            pass

        return bRet

    """============================================================================================
    函数名称: getProtocalInfo
    功能描述: 获取测试结果详情
    参数列表: url——请求url路径；
              method——请求方法：get、post、put、delete；
              query_param——请求Query；
              need_sid——是否需要SID(session id), 1：需要 0：不需要；
              reqXmlFilename——请求xml模板文件名；
              respXmlFilename——期望Response的xml模板文件名；
    返回结果: 当前接口的ISAPI信息, 如/ISAPI/Bumblebee/Device/Encoders,POST,SID,MT=GET,EncodersRequest_GET.xml
    ==============================================================================================="""

    def getProtocalInfo(self, url, method, query_param, need_sid, reqXmlFilename, respXmlFilename=''):
        if need_sid == 1:
            if query_param == '':
                query_param = 'SID'
            else:
                query_param = '(SID,%s)' % (query_param)
        else:
            pass

        # 组装protocal
        req_xml_filename = reqXmlFilename + '.xml' if reqXmlFilename else ''
        resp_xml_filename = respXmlFilename + '.xml' if respXmlFilename else ''
        protocalInfo = ','.join([url, method, query_param])
        return protocalInfo + ',' + req_xml_filename + ',' + resp_xml_filename + ',' + self.conn.elapsed

    """============================================================================================
    函数名称: convertDataList
    功能描述: 数据列表转换,将data_list中不确定的数据根据字典pendData_dict转换
    参数列表: data_list——请求xml模板所需字段的数据列表,默认为空;
              pendData_dict——数据列表中不确定数据的字典,如{$EncoderID:1, $CameraID: 5},默认为空;
              xmlType——转换模板的类型,默认为Request
    返回结果: data_list,替换后的数据结果列表
    ==============================================================================================="""

    def convertDataList(self, data_list=[], pendData_dict={}, xmlType="Request"):
        if len(pendData_dict) > 0:
            if xmlType == "Request":
                for data in pendData_dict:
                    if '$PW' in data:  # 测试数据列表包含需要进行AES加密的字段,$PW
                        value = pendData_dict[data]
                        pendData_dict[data] = self.conn.Encrypt(value, self.loginPw)
                    elif '$RSA_PW' in data:  # 测试数据列表包含需要进行RSA加密的字段, $RSA_PW
                        value = pendData_dict[data]
                        pendData_dict[data] = self.conn.RSA_Encrypt(value)
                    else:
                        pass
                data_list = DataProcess().convert_params_list(data_list, pendData_dict)
            else:
                data_list = DataProcess().convert_params_list(data_list, pendData_dict)
        else:
            pass

        return data_list

    """============================================================================================
    函数名称: packageData
    功能描述: 组装xml模板与数据
    参数列表:xmlFilename——请求xml模板文件名,默认为空；
             data_list——请求xml模板所需字段的数据列表,默认为空;
             xmlType——xml模板类型,默认为Request
    返回结果: 模板与数据组装后的字符串
    ==============================================================================================="""

    def packageData(self, xmlFilename='', data_list=[], xmlType="Request"):
        # 组装xml
        if xmlFilename == '':
            packXml = ""
        else:
            # 根据请求xml路径，构造xml组装对象
            xmlp = XmlPacker(xmlFilename + '.xml', xmlType)
            # 组装请求xml模板与数据
            packXml = xmlp.get(data_list)

        return packXml

    """============================================================================================
    函数名称: sendRequest
    功能描述: 发送请求
    参数列表: index——相同协议发送序号;
              url——请求url路径；
              method——请求方法：get、post、put、delete；
              query_param——请求Query；
              need_sid——是否需要SID(session id), 1：需要 0：不需要；
              reqXmlFilename——请求xml模板文件名；
              reqData_list——请求xml模板所需字段的数据列表,默认为空；
              reqPendData_dict——数据列表中不确定数据的字典,如{$EncoderID:1, $CameraID: 5},默认为空；
              respData_dict——自定义需要比较的期望值字典, 如{xpath: [期望值]},默认为空不比较指定字段；
              respPendData_dict——期望值列表中不确定的数据的字典, 如{$EncoderID:1, $CameraID: 5}
              send_overtime——超时时间, 默认30s;
              recv_overtime——接收超时时间, 默认30s;
    返回结果: 比较结果     
    ==============================================================================================="""

    def sendRequest(self, index, url, method, query_param, need_sid=1,
                    reqXmlFilename='', reqData_list=[], reqPendData_dict={},
                    respData_dict={}, respPendData_dict={}, send_overtime=30000, recv_overtime=30000):
        # 请求数据转换
        reqData_list = self.convertDataList(reqData_list, reqPendData_dict)

        # 组装发送请求数据
        reqXml = self.packageData(reqXmlFilename, reqData_list)

        # 发送请求接收响应
        actualRespXml = self.conn.cmd(url, method, query_param, need_sid, reqXml, send_overtime, recv_overtime)

        # 校验并返回测试结果
        self.respXmlParse = XmlParser(actualRespXml)
        protocolInfo = self.getProtocalInfo(url, method, query_param, need_sid, reqXmlFilename)
        return self.recordTestResult(*(
            XmlVerify().responseCompare(protocolInfo, reqXml, actualRespXml, respData_dict, respPendData_dict, index)))

    """============================================================================================
    函数名称: sendRequest2
    功能描述: 发送请求
    参数列表: index——相同协议发送序号;
              url——请求url路径；
              method——请求方法：get、post、put、delete；
              query_param——请求Query；
              need_sid——是否需要SID(session id), 1：需要 0：不需要；
              reqXmlFilename——请求xml模板文件名；
              reqData_list——请求xml模板所需字段的数据列表,默认为空；
              reqPendData_dict——数据列表中不确定数据的字典,如{$EncoderID:1, $CameraID: 5},默认为空；
              expRespXmlFilename——期望响应xml模板文件名,默认为空；
              expRespData_list——期望响应xml模板所需字段的数据列表,默认为空；
              respPendData_dict——期望值列表中不确定的数据的字典, 如{$EncoderID:1, $CameraID: 5}
              send_overtime——超时时间, 默认30s;
              recv_overtime——接收超时时间, 默认30s;
    返回结果: 比较结果     
    ==============================================================================================="""

    def sendRequest2(self, index, url, method, query_param, need_sid=1,
                     reqXmlFilename='', reqData_list=[], reqPendData_dict={},
                     expRespXmlFilename='', expRespData_list=[], respPendData_dict={}, send_overtime=30000,
                     recv_overtime=30000):
        # 请求数据转换
        reqData_list = self.convertDataList(reqData_list, reqPendData_dict)

        # 组装发送请求数据
        reqXml = self.packageData(reqXmlFilename, reqData_list)

        # 发送请求接收响应
        actualRespXml = self.conn.cmd(url, method, query_param, need_sid, reqXml, send_overtime, recv_overtime)

        # 期望数据转换
        expRespData_list = self.convertDataList(expRespData_list, respPendData_dict, 'Response')

        # 组装期望响应数据
        expRespXml = self.packageData(expRespXmlFilename, expRespData_list, 'Response')

        # 校验并返回测试结果
        self.respXmlParse = XmlParser(actualRespXml)
        protocolInfo = self.getProtocalInfo(url, method, query_param, need_sid, reqXmlFilename, expRespXmlFilename)
        return self.recordTestResult(
            *(XmlVerify().responseCompare2(protocolInfo, reqXml, expRespXml, actualRespXml, index)))

    """============================================================================================
    函数名称: sendRequest_ParamsList
    功能描述: 根据参数列表，发送请求
    参数列表: params_list——接口参数列表;
    返回结果: 比较结果     
    ==============================================================================================="""

    def sendRequest_ParamsList(self, params_list):
        (index, url, method, query_param, need_sid, reqXmlFilename, reqData_list, reqPendData_dict, respData_dict,
         respPendData_dict) = params_list
        self.sendRequest(index, url, method, query_param, need_sid, reqXmlFilename, reqData_list, reqPendData_dict,
                         respData_dict, respPendData_dict)

    """============================================================================================
    函数名称: getSpecifiedData
    功能描述: 发送GET请求, 获取指定xpath下指定字段为指定值节点下的, 要查找字段的数值
    参数列表: query_params_list——GET请求数据列表；xpath——xpath路径；findTagName——需要查找的标签名；
              tagName——指定的标签名；value——tagName的值
    返回结果: 数据(字符串)    
    ==============================================================================================="""

    def getSpecifiedData(self, query_params_list, xpath, findTagName, tagName, value):
        # 先刷新
        self.sendRequest_ParamsList(query_params_list)
        # 再获取数据
        return self.respXmlParse.get_value_by_specified_tagName(xpath, findTagName, tagName, value)

    """============================================================================================
    函数名称: getSpecifiedDataList
    功能描述: 发送GET请求, 获取指定xpath下指定标签下的所有数据
    参数列表: query_params_list——GET请求数据列表；xpath——xpath路径；findTagName——需要查找的标签名 
    返回结果: 数据列表  
    ==============================================================================================="""

    def getSpecifiedDataList(self, query_params_list, xpath, findTagName):
        # 先刷新
        self.sendRequest_ParamsList(query_params_list)
        # 再获取数据列表
        return self.respXmlParse.get_value_list_by_specified_tagName(xpath, findTagName)

    """============================================================================================
    函数名称: getSpecifiedDataList1(新增，包含getSpecifiedDataList方法的功能)
    功能描述: 发送GET请求, 获取指定xpath下指定标签下的所有数据
    参数列表: query_params_list——GET请求数据列表；xpath——xpath路径；findTagName——需要查找的标签名
              tagName——指定的标签；value——tagName的值(指定标签为空，则查找xpath节点下的标签为findTagName的所有值)
    返回结果: 数据列表  
    ==============================================================================================="""

    def getSpecifiedDataList1(self, query_params_list, xpath, findTagName, tagName='', value=''):
        # 先刷新
        self.sendRequest_ParamsList(query_params_list)
        # 再获取数据列表
        return self.respXmlParse.get_dataList_by_specified_tagName(xpath, findTagName, tagName, value)

    """============================================================================================
    函数名称: getSpecifiedDataList2
    功能描述: 发送GET请求, 获取指定xpath下指定标签下的所有数据
    参数列表: query_params_list——GET请求数据列表；xpath——xpath路径；tagName——指定的标签；value——tagName的值
              findXpath——定位指定xpath的节点路径; findTagName——需要查找的标签名
    返回结果: 数据列表  
    ==============================================================================================="""

    def getSpecifiedDataList2(self, query_params_list, xpath, tagName, value, findXpath, findTagName):
        # 先刷新
        self.sendRequest_ParamsList(query_params_list)
        # 再获取数据列表
        return self.respXmlParse.get_value_list_by_specified_xpath(xpath, tagName, value, findXpath, findTagName)
