# -*- coding: utf-8 -*-

"""==================================================================
Copyright(c) 2016-2017 Hangzhou Hikvision Digital Technology Co.,Ltd
文件名称:  Util.py
简要描述： 通用方法模块，提供如ini文件解析、xml文件解析、日志文件记录等类
作    者： Qiu Jiangping
完成日期:  2017-5-11
修订说明:
=================================================================="""

from xml.etree import ElementTree as ET
import string
import traceback
import sys, os
# import cStringIO
import time, datetime
import re
# import ConfigParser
from .XmlReader import *
from .DomXmlParse import *

global param_list
param_list = []
for i in range(0, 63):
    param_list.append('p' + str(i + 1))

# 测试框架启动根路径
global g_rootPath
g_rootPath = os.getcwd()
if '\\Lib' in g_rootPath:
    g_rootPath = g_rootPath.replace('\\Lib', '')
else:
    pass


# 数据处理类
class DataProcess:
    def __init__(self):  # 初始化
        pass

    def __del__(self):
        pass

    """======================================================================
    函数名称: convert_params_list
    功能描述: 对列表中$标注的字段进行替换
    参数列表: *listArg——列表, listArg[0]为xml字段列表；listArg[1]为映射关系    
    返回结果: 无  
    ======================================================================="""

    def convert_params_list(self, *listArg):
        rep = [listArg[1][x] if x in listArg[1] else x for x in listArg[0]]
        return rep


# 时间转换类
class DateTimeConvert(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    """======================================================================
    函数名称: utc2local
    功能描述: UTC时间转本地时间(+8:00)
    参数列表: utc_st-utc时间  
    返回结果: 本地时间
    ======================================================================="""

    def utc2local(self, utc_st):
        now_stamp = time.time()
        local_time = datetime.datetime.fromtimestamp(now_stamp)
        utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
        offset = local_time - utc_time
        local_st = utc_st + offset
        return local_st

    """======================================================================
    函数名称: local2utc
    功能描述: 本地时间转UTC时间(+8:00)
    参数列表: utc_st-utc时间  
    返回结果: 本地时间
    ======================================================================="""

    def local2utc(self, local_st):
        time_struct = time.mktime(local_st.timetuple())
        utc_st = datetime.datetime.utcfromtimestamp(time_struct)
        return utc_st


# ini 配置文件解析类
# class IniFileParser:
#     def __init__(self, filePath=g_rootPath + '\\TestConfig\\Config.ini'):
#         self.config = ConfigParser.ConfigParser()
#         with open(filePath, 'rb') as configFile:
#             self.config.readfp(configFile)
#
#     def __del__(self):
#         pass
#
#     """======================================================================
#     函数名称: getConfigInformation
#     功能描述：读取配置文件，获取相关数据
#     参数列表: section——表示配置文件中配置项模块, 例如 [VSM_Server]
#               param_list——表示配置文件中的参数
#     返回结果: 返回配置文件中对应值列表
#     ======================================================================="""
#
#     def getConfigInformation(self, section, param_list):
#         value_list = []
#         for para in param_list:
#             value_list.append(self.getConfigValue(section, para))
#
#         return value_list
#
#     """======================================================================
#     函数名称: getConfigValue
#     功能描述：读取配置文件，获取相关数据
#     参数列表: section——表示配置文件中配置项模块, 例如 [VSM_Server]
#               param——表示配置文件中的参数
#     返回结果: 返回配置文件中对应的值
#     ======================================================================="""
#
#     def getConfigValue(self, section, param):
#         value = self.config.get(section, param)
#         # 一些值需要转成整型
#         if param in ['port', 'clientType']:
#             value = int(value)
#         else:
#             pass
#
#         return value
#
#     """======================================================================
#     函数名称: get_config_params_dict
#     功能描述：读取配置文件, 获取配置参数字典
#     参数列表: section_list——表示配置文件中配置项列表
#               key_list——表示配置文件中的参数列表
#     返回结果: 返回配置文件中对应的值
#     ======================================================================="""
#
#     def get_config_params_dict(self, section_list=[], key_list=[]):
#         config_params_dict = {}
#         try:
#             for section in section_list:
#                 params_value_list = self.getConfigInformation(section, key_list)
#                 config_params_dict[section] = params_value_list
#         except:
#             traceback.print_exc()
#             error_info = '=============== Parse Config.ini file error ===============\r'
#             print
#             error_info
#             g_logRecord.writeText2Log(error_info, 2)
#             os._exit(1)
#
#         return config_params_dict


# 将打印信息重定向到各种流，如控制台、文件、内存等
# class LogRedirect:
#     def __init__(self):
#         self.content = ''
#         self.savedStdout = sys.stdout
#         self.memObj, self.fileObj, self.nulObj = None, None, None
#
#     def __del__(self):
#         pass
#
#     # 外部的print语句将执行本write()方法，并由当前sys.stdout输出
#     def write(self, outStr):
#         # self.content.append(outStr)
#         self.content += outStr
#
#     # 标准输出重定向至控制台
#     def toCons(self):
#         sys.stdout = self.savedStdout  # sys.__stdout__
#
#     # 标准输出重定向至内存
#     def toMemo(self):
#         self.memObj = cStringIO.StringIO()
#         sys.stdout = self.memObj
#
#     # 标准输出重定向至文件
#     def toFile(self, filename):
#         self.fileObj = open(filename, 'a+', 1)  # 改为行缓冲
#         sys.stdout = self.fileObj
#
#     # 抑制输出
#     def toMute(self):
#         self.nulObj = open(os.devnull, 'w')
#         sys.stdout = self.nulObj
#
#     def restore(self):
#         self.content = ''
#         if self.memObj.closed != True:
#             self.memObj.close()
#         if self.fileObj.closed != True:
#             self.fileObj.close()
#         if self.nulObj.closed != True:
#             self.nulObj.close()
#         sys.stdout = self.savedStdout  # sys.__stdout__


# log记录类
class LogRecord:
    def __init__(self):
        self.logfile = g_rootPath + '\\TestReport\\log.txt'
        self.initLogFile()

    def __del__(self):
        pass

    def initLogFile(self):
        dateTime = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.logfile, 'w') as logFile:
            logFile.write('=============== [' + str(dateTime) + ', Begin to record...] ===============\r')

    def writeText2Log(self, strContent, log_type=0):
        log_prefix = ''
        if log_type == 0:
            log_prefix = 'Info'
        elif log_type == 1:
            log_prefix = 'Warning'
        else:
            log_prefix = 'Error'

        with open(self.logfile, 'a+', 1) as logFile:
            logFile.write('[%s]: %s\r%s\r' % (log_prefix, time.strftime("%Y-%m-%d %H:%M:%S"), strContent))


# 定义日志全局变量
#g_logType = ''.join(IniFileParser().getConfigInformation('LogSetting', ['logRecordType']))
g_logRecord = LogRecord()
# 错误码xml文档解析对象
# error_xml_parse = XmlReader(g_rootPath + u'\\Doc\\协议文档\\ErrorCode.xml')

# 获取登录参数(配置文件只读一次)
# g_login_params_dict = IniFileParser().get_config_params_dict(
#     ['VSM_Server', 'RSM_Server', 'Control_Client', 'VSM_Control_Client'],
#     ['ip', 'port', 'username', 'password', 'clientType'])
# g_login_db_params_dict = IniFileParser().get_config_params_dict(['VSM_DB', 'RSM_DB'],
#                                                                 ['db_name', 'db_ip', 'db_port', 'db_username',
#                                                                  'db_password'])


# XML简单解析类
class XmlParser:
    def __init__(self, text):  # 用字符串初始化
        xmlstr_ = text
        try:
            self.root = ET.fromstring(text)
        except:
            # 捕捉Response为空的处理
            self.root = ET.fromstring(
                '<ResponseStatus><ErrorModule>9999</ErrorModule><ErrorCode>9999</ErrorCode></ResponseStatus>')

    def __del__(self):
        pass

    # 获取path节点数
    def get_cnt(self, xmlpath):
        nodes = self.root.findall(xmlpath)
        return len(nodes)

    # 获取path节点值
    def get_v(self, xmlpath, pos=0):
        try:
            node = self.root.findall(xmlpath)[pos]
            return node.text
        except:
            traceback.print_exc()
            return 'none (can not get value)'

    # 获取Xpath节点值,返回整形
    def get_int_v(self, xmlpath, pos=0):
        try:
            return int(self.get_v(xmlpath, pos))
        except:
            traceback.print_exc()
            print(u'参数没有包含数字\n')
            return -1

    # 获取Xpath节点值,返回整形
    def get_a(self, xmlpath, attrb, pos=0):  # 获取path节点属性
        node = self.root.findall(xmlpath)[pos]
        nodeattr = ''
        if node.attrib.has_key(attrb) > 0:
            nodeattr = node.attrib[attrb]
        return nodeattr

        # 获取path节点值,返回整形

    def get_int_a(self, xmlpath, attrb, pos=0):
        return int(self.get_a(xmlpath, attrb, pos))

    # 获取原始字符串
    def get_str(self):
        return ET.tostring(self.root, encoding="utf-8", method="xml")

    """=========================================================
    函数名称: getResponseHeader
    功能描述: 获取Response数据头      
    参数列表: 无      
    返回结果: 错误模块错误码元组，如('0', '0')      
    ============================================================"""

    def getResponseHeader(self):
        strEm = self.get_v('ErrorModule')
        strEc = self.get_v('ErrorCode')
        return (strEm, strEc)

    """=========================================================
    函数名称: indent
    功能描述: 将xml文本缩进对齐       
    参数列表: level——节点等级       
    返回结果:       
    ============================================================"""

    def indent(self, node, level=0):
        i = "\n" + level * "  "
        if len(node):
            if not node.text or not node.text.strip():
                node.text = i + "  "
            if not node.tail or not node.tail.strip():
                node.tail = i

            for elem in node:
                XmlParser.indent(self, elem, level + 1)
            if not node.tail or not node.tail.strip():
                node.tail = i
        else:
            if level and (not node.tail or not node.tail.strip()):
                node.tail = i

    """=========================================================
    函数名称: getXmlDataAfterIndent
    功能描述: 获取xml文本缩进对齐后的文本      
    参数列表:       
    返回结果: strData     
    ============================================================"""

    def getXmlDataAfterIndent(self):
        self.indent(self.root)
        strData = self.get_str()
        if '<?xml version=\'1.0\' encoding=\'utf8\'?>' in strData:
            strData = strData.replace('<?xml version=\'1.0\' encoding=\'utf8\'?>', '')

        if ' />' in strData:
            strData = strData.replace(' />', '/>')

        return strData

    """=========================================================
    函数名称: traverseFindNode
    功能描述: 遍历节点，定位指定的标签名及其值下的目标节点
    参数列表: node——待遍历的根节点；findNodeAttr——指定的标签名及其值的元组，
              如('Name', 'Test')，即<Name>Test</Name>
    返回结果: 无     
    ============================================================"""

    def traverseFindNode(self, node, findNodeAttr):
        children_node = node.getchildren()
        node_count = len(children_node)
        if node_count == 0:
            try:
                if findNodeAttr == (node.tag, node.text):
                    self.bFound = True
            except:
                traceback.print_exc()

        for child in children_node:
            self.traverseFindNode(child, findNodeAttr)

    """==============================================================================
    函数名称: get_value_by_specified_tagName
    功能描述: 查找标签名为findTagName对应的值(根据Name找ID)
              如在xpath为Data/EncoderLsit节点下，找到包含<Name>Test</Name>的目标节点，
              在该目标节点下，找到需要查找的标签如<ID>的值
    参数列表: xpath——xpath路径；findTagName——需要查找的标签名；
              tagName——指定的标签名，value——指定的标签名对应的值，如<Name>Test</Name>     
    返回结果: 指定字段的值
    ================================================================================="""

    def get_value_by_specified_tagName(self, xpath, findTagName, tagName, value):
        self.bFound = False
        # 根据xpath获得目标节点列表
        nodeList = self.root.findall(xpath)
        strVal = "-1"
        for node in nodeList:
            # 遍历查找包含tagName，value的目标节点
            self.traverseFindNode(node, (tagName, value))
            if self.bFound == True:
                try:
                    # 找到目标节点，提取值
                    strVal = node.find(findTagName).text
                except:
                    traceback.print_exc()
                    # g_logRecord.writeText2Log('xpath error: %s, can not get the value of tagname: %s\r'%(xpath, findTagName))
                break
            else:
                pass

        return strVal

    """=========================================================
    函数名称: traverseGetDataList
    功能描述: 遍历节点，定位指定的标签名及其值下的目标节点，提取查找标签名为findTagName对应的所有值
    参数列表: node——待遍历的根节点；findTagName——需要查找的标签名；
    返回结果: 无     
    ============================================================"""

    def traverseGetDataList(self, node, findTagname):
        children_node = node.getchildren()
        node_count = len(children_node)
        if node_count == 0:
            if node.tag == findTagname:
                try:
                    self.data_list.append(node.text)
                except:
                    traceback.print_exc()

        for child in children_node:
            self.traverseGetDataList(child, findTagname)

    """============================================================================================
    函数名称: get_value_list_by_tagname_list
    功能描述: 查找标签名列表查找对应的所有值列表
    参数列表: xpath——xpath路径；tagname_list——指定的标签名列表   
    返回结果: 列表       
    ==============================================================================================="""

    def get_value_list_by_tagname_list(self, xpath, tagname_list):
        try:
            value_list = []
            for tagname in tagname_list:
                temp_list = self.get_value_list_by_specified_tagName(xpath, tagname)
                value_list.append(temp_list[0])
            return value_list
        except:
            traceback.print_exc()

    """============================================================================================
    函数名称: get_dataList_by_specified_tagName
    功能描述: 查找标签名为findTagName对应的所有值(根据ID找Name)
              如在xpath为Data/EncoderLsit节点下，找到包含<ID>1</ID>的目标节点，
              在该目标节点下，找到需要查找的标签如<Name>的所有值
    参数列表: xpath——xpath路径；findTagName——需要查找的标签名；
              tagName——指定的标签名，value——指定的标签名对应的值，如<ID>1</ID>     
    返回结果: 指定字段的值
    ==============================================================================================="""

    def get_dataList_by_specified_tagName(self, xpath, findTagName, tagName, value):
        # 根据xpath获得目标节点列表
        nodeList = self.root.findall(xpath)
        self.data_list = []
        for node in nodeList:
            if tagName == '':  # 无指定标签，提取xpath节点下所有标签为findTagName对应的值
                try:
                    self.traverseGetDataList(node, findTagName)
                except:
                    traceback.print_exc()
            else:  # 指定标签，根据指定标签及其值定位目标节点，再提目标节点下所有标签为findTagName对应的值
                try:
                    if node.find(tagName).text == value:
                        self.traverseGetDataList(node, findTagName)
                    else:
                        pass
                except:
                    traceback.print_exc()

        return self.data_list

    """============================================================================================
    函数名称: get_value_list_by_specified_xpath
    功能描述: 查找标签名为findTagName对应的所有值
              如在xpath为Data/EncoderLsit/Encoder的节点下, 找到包含<ID>1</ID>的子节点，
              再根据findxpath，查找标签为如<Name>对应的所有值列表
    参数列表: xpath——xpath路径；tagName——指定的标签名；value——指定标签名对应的值；
              findXpath——需要查找的xpath；findTagName——需要查找的标签名      
    返回结果: 列表       
    ==============================================================================================="""

    def get_value_list_by_specified_xpath(self, xpath, tagName, value, findXpath, findTagName):
        nodeList = self.root.findall(xpath)
        strValue_list = []
        for node in nodeList:
            try:
                if node.find(tagName).text == value:
                    xpath = xpath + '/' + findXpath
                    strValue_list = self.get_value_list_by_specified_tagName(xpath, findTagName)
                    break
            except:
                traceback.print_exc()
                g_logRecord.writeText2Log(
                    'xpath error: %s, can not get the value of tagname: %s\r' % (xpath, findTagName), 2)

        return strValue_list

    """============================================================================================
    函数名称: get_value_list_by_specified_tagName
    功能描述: 查找标签名为findTagName对应的所有值
              如在xpath为Data/EncodersList/Encoder节点下,查找所有标签名为ID对应的值
    参数列表: xPath——xpath路径；findTagName——需要查找的标签名       
    返回结果: 标签名为findTagName对应的所有值列表    
    ==============================================================================================="""

    def get_value_list_by_specified_tagName(self, xpath, findTagName):
        if findTagName != '':
            xpath = xpath + '/' + findTagName
        nodeList = self.root.findall(xpath)
        find_list = []
        for node in nodeList:
            try:
                strVal = node.text
                find_list.append(strVal)
            except:
                traceback.print_exc()
                g_logRecord.writeText2Log(
                    'xpath error: %s, can not get the value of tagname: %s\r' % (xpath, findTagName), 2)

        return find_list

    """============================================================================================
    函数名称: saveResponseXml
    功能描述: 保存Response Xml到文件;
    参数列表: strFilename——文件名;
              strContent——文件内容;
    返回结果: 无
    ==============================================================================================="""

    def saveResponseXml(self, strFilename, strContent):
        with open(g_rootPath + '\\TestReport\\ActualResponse\\%s.xml' % (strFilename), 'w') as responseXmlFile:
            responseXmlFile.write(strContent)


# XML简单组装类
class XmlPacker:
    """============================================================================================
    函数名称: __init__
    功能描述: 初始化xml模板
    参数列表: xmlFilename——xml模板名称；
              xmlType——xml模板类型,默认为Request;
              mode——组装方式
    返回结果: 无
    ==============================================================================================="""

    def __init__(self, xmlFilename, xmlType='Request', mode=False):
        self.curFilePath = (g_rootPath + '\\XmlTemplate\\%s\\') % (xmlType == 'Request' and 'Request' or 'Response')
        self.param_list = param_list
        self.reconf(xmlFilename, mode)

    def __del__(self):
        pass

    """============================================================================================
    函数名称: reconf
    功能描述: 初始化xml模板
    参数列表: xmlFilename——xml模板名称；
              mode——组装方式,True表示xmlFilePath为xml文本内容, False表示xmlFilePath为路径    
    返回结果: 无     
    ==============================================================================================="""

    def reconf(self, xmlFilename, mode=False):  # 重置xml模板
        s = ""
        if mode:
            s = xmlFilename
        else:
            # 模板化xml文件并替换，并获取替换后的文本与param_list
            xmlConvert = XmlReader(self.curFilePath + xmlFilename)
            (s, self.param_list) = xmlConvert.Templatize()

        self.xml_t = string.Template(s)

    """============================================================================================
    函数名称: get
    功能描述: 组装xml模板
    参数列表: param——模板字段所需的数据
    返回结果: 无     
    ==============================================================================================="""

    def get(self, param):  # 获取xml
        p_dict = dict(zip(self.param_list, param))
        return self.xml_t.safe_substitute(p_dict)


# XML校验类
class XmlVerify:
    def __init__(self):
        self.xmlCmp_Dict = {
            'Tag': u'标签不一致',
            'Value': u'数值不一致',
            'Count': u'拥有子节点个数不一致',
        }
        (self.bResult, self.strFailReason) = (True, '')

    def __del__(self):
        pass

    """============================================================================================
    函数名称: log2File
    功能描述: 记录发送与接收详细数据到日志文件log.txt
    参数列表: protocalInfo——当前接口的ISAPI信息, 如/ISAPI/Bumblebee/Areas_GET；
              bResult——校验结果; 
    返回结果: 无    
    ==============================================================================================="""

    def log2File(self, protocalInfo, bResult):
        # 发送请求数据
        try:
            strReqData = self.reqXmlParser.getXmlDataAfterIndent()
            # 发送请求为空
            if '<ErrorModule>9999</ErrorModule>' in strReqData:
                strReqData = 'RequestData: None\n'
            else:
                pass
        except:
            traceback.print_exc()
            strReqData = 'RequestData is empty (Current xml template is empty or contains invalid character)\r'

        verify_status = 'Pass' if bResult else 'Fail'
        strReqXmlData = ('=============== [%s] [Send Request]: %s =============== \r%s') % (
        verify_status, protocalInfo, strReqData)
        # 实际接收的响应数据
        strActualRespXmlData = ('=============== [Receive Response] =============== \r%s\n') % (
            self.actualRespXmlParser.getXmlDataAfterIndent())

        # 日志记录控制
        # if g_logType == '0':
        #     g_logRecord.writeText2Log(strReqXmlData + strActualRespXmlData)
        # else:
        #     if bResult == False:
        #         g_logRecord.writeText2Log(strReqXmlData + strActualRespXmlData)
        #     else:
        #         pass

        # 打印发送请求数据
        print('{%s,%s,%s}' % (verify_status, protocalInfo, '' if bResult else '\r%s' % (self.strFailReason)))

    """============================================================================================
    函数名称: compare_response_xml
    功能描述: 比较两个xml文本是否相同
    参数列表: expRespXml——期望返回xml文本
              key_info——xpath
    返回结果: 无    
    ==============================================================================================="""

    def compare_response_xml(self, expRespXml):
        # 提取期望xml的xpath及对应值
        domXml = DomXmlParse(expRespXml, True)
        expect_dict = domXml.get_xpath_value_dict()

        # 遍历提取(xpath: 数值), 对比实际响应xml数据
        bResult, strFailReason = True, ''
        fail_reason_list = []
        for (xpath, value) in expect_dict.items():
            # 提取xpath及下标
            pos = 0
            group_list = re.findall(r'\[\d+\]', xpath)
            if group_list:
                elem = group_list[0]
                pos = (int)(elem.strip('[').strip(']'))
                xpath = xpath.replace(elem, '')
            else:
                pass

            # 实际响应xml中提取对应xpath下的路径
            actual_value = self.actualRespXmlParser.get_v(xpath, pos)
            if value != actual_value:
                bResult = False
                fail_reason_list.append(('[XPath]: %s; [Expect]: %s; [Actual]: %s') % (xpath, value, actual_value))
            else:
                pass

        strFailReason = '\r'.join(fail_reason_list)
        return (bResult, strFailReason)

    """============================================================================================
    函数名称: responseCompare
    功能描述: 比较Response实际收到(ErrorModule,ErrorCode)是否为('0', '0')
    参数列表: protocalInfo——当前接口的ISAPI信息, 如/ISAPI/Bumblebee/Areas_GET；
              reqXml——请求xml文本；
              actualRespXml——实际收到的相应数据；
              respData_dict——自定义需要比较的期望值字典, 如{xpath: [期望值]},默认为空不比较指定字段;
              respPendData_dict——期望值列表中不确定的数据的字典, 如{$EncoderID:1, $CameraID: 5},默认为空
              index——相同接口测试协议的发送序号,用于提取对应的期望数据列表中的期望值; 
    返回结果: (标记, 原因)    
    ==============================================================================================="""

    def responseCompare(self, protocalInfo, reqXml, actualRespXml, respData_dict={}, respPendData_dict={}, index=0):
        # 创建xml解析器
        self.reqXmlParser = XmlParser(reqXml)
        self.actualRespXmlParser = XmlParser(actualRespXml)
        # 实际返回数据头信息
        (errModule, errCode) = self.actualRespXmlParser.getResponseHeader()
        if (errModule, errCode) == ('0', '0'):
            self.bResult = True
        else:
            self.bResult = False
            # 提取错误详情
            # (em_desc, ec_desc) = error_xml_parse.get_desc_by_xpath('ErrorModule/Module', errModule, errCode)
            # self.strFailReason = ('    [Expect]: ErrorCode=0; ErrorModule=0') + '\r' + \
            #                      ('    [Actual]: ErrorCode=%s(%s); ErrorModule=%s(%s)') % (
            #                      errCode, ec_desc, errModule, em_desc)

        # 记录发送与接收详细数据到日志文件log.txt
        self.log2File(protocalInfo, self.bResult)

        # 返回比较结果信息
        return (self.bResult, ('\r[%s] %s\r') % (index, protocalInfo) + self.strFailReason)

    """============================================================================================
    函数名称: responseCompare2
    功能描述: 期望xml数据与实际接收到的xml数据进行比较
    参数列表: protocalInfo——当前接口的ISAPI信息, 如/ISAPI/Bumblebee/Areas_GET；
              reqXml——请求xml文本；
              expRespXml——期望响应Xml文本；
              actualRespXml——实际响应文本；
              index——相同接口测试协议的发送序号,用于提取对应的期望数据列表中的期望值; 
    返回结果: (标记, 原因)    
    ==============================================================================================="""

    def responseCompare2(self, protocalInfo, reqXml, expRespXml, actualRespXml, index=0):
        if actualRespXml == None:  # 服务器数据返回为空
            self.bResult = False
            self.strFailReason = ('[Expect]: No ErrorCode') + '\r' + \
                                 ('[Actual]: Return No Data')
        else:
            # 创建xml解析器
            self.reqXmlParser = XmlParser(reqXml)
            self.actualRespXmlParser = XmlParser(actualRespXml)
            # 实际返回数据头信息
            (errModule, errCode) = self.actualRespXmlParser.getResponseHeader()
            if (errModule, errCode) == ('0', '0'):
                self.bResult, self.strFailReason = self.compare_response_xml(expRespXml)
            else:
                self.bResult = False
                # 提取错误详情
                (em_desc, ec_desc) = error_xml_parse.get_desc_by_xpath('ErrorModule/Module', errModule, errCode)
                self.strFailReason = ('    [Expect]: ErrorCode=0; ErrorModule=0') + '\r' + \
                                     ('    [Actual]: ErrorCode=%s(%s); ErrorModule=%s(%s)') % (
                                     errCode, ec_desc, errModule, em_desc)

        # 记录发送与接收详细数据到日志文件log.txt
        self.log2File(protocalInfo, self.bResult)

        # 返回比较结果信息
        return (self.bResult, ('\r[%s] %s\r') % (index, protocalInfo) + self.strFailReason)
