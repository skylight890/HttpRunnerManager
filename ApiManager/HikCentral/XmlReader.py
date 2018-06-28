# coding: utf-8

"""==================================================================
Copyright(c) 2015-2016 Hangzhou Hikvision Digital Technology Co.,Ltd
文件名称:  XmlReader.py
简要描述： 用于xml文件的解析、节点的增删改查功能
作    者： Qiu Jiangping 
完成日期:  2017-5-8
修订说明: 
=================================================================="""

import traceback
import xml.etree.ElementTree as ET #(将模块赋值给变量ET，模块名太长或你讨厌模块名)

class XmlReader:
    """=========================================================
    函数名称: __init__
    功能描述: 初始化解析xml文件
    参数列表: xml_path——xml路径         
    返回结果:                  
    ============================================================"""  
    def __init__(self, xml_path="CmsExpressRequest.xml"):
        self.curFilepath = xml_path
        self.param_list  = []
        (self.bFileEmpty, self.xmlTree) = self.read_xml(xml_path)
        self.pos = 1
        self.cnt = 1
    
    """=========================================================
    函数名称: get_xmltree
    功能描述: 返回当前xml文件的树结构
    参数列表:                 
    返回结果: self.xmlTree        
    ============================================================"""     
    def get_xmltree(self):
        return self.xmlTree
    
    """=========================================================
    函数名称: read_xml
    功能描述: 读取并解析xml文件         
    参数列表: xml_path——xml路径        
    返回结果: self.xmlTree           
    ============================================================"""  
    def read_xml(self, xml_path):
        bEmpty = False
        xmlTree = ET.ElementTree()
        try:
            xmlTree.parse(xml_path)  
        except:
            # 捕捉xml文件为空的异常处理
            traceback.print_exc()
            print('%s is empty or contains invalid character'%xml_path)
            bEmpty = True
            
        return (bEmpty, xmlTree)
    
    """=========================================================
    函数名称: write_xml
    功能描述: 保存xml文件         
    参数列表: out_path——xml保存路径        
    返回结果:        
    ============================================================"""  
    def write_xml(self, out_path):  
        self.xmlTree.write(out_path, encoding="utf-8",xml_declaration=False)
                
    """=========================================================
    函数名称: walkNode
    功能描述: 遍历修改节点text为$pi，并保存模板数据比列表   
    参数列表: node——需要遍历的节点；    
    返回结果: 无         
    ============================================================"""                
    def walkNode(self, node):
        children_node = node.getchildren()
        node_count = len(children_node)
        # 是否为节点
        if node_count == 0:
            # 根据属性查找节点
            tagName = node.tag
            text = node.text
            if text != '' and text != None:
                if '$p' in text: # 模板是否已经包含$p
                    # 提取下标
                    index = int(text.split('$p')[-1])
                    if index == self.pos: #下标与当前计数一致
                        self.param_list.append(text.replace('$',''))
                        self.cnt = self.cnt + 1
                    else:
                        node.text = '$p' + str(self.pos)
                        self.param_list.append('p'+ str(self.pos))
                else:
                    node.text = '$p' + str(self.pos)
                    self.param_list.append('p'+ str(self.pos))
                
                self.pos = self.pos + 1   
                
        for child in children_node:
            XmlReader.walkNode(self, child)
        
        return self.param_list
     
    """=========================================================
    函数名称: Templatize
    功能描述: 将目标xml文件模板化
    参数列表:       
    返回结果: 无         
    ============================================================"""
    def Templatize(self):
        if self.bFileEmpty == True:
          return ('', [])
        else:
            pos = 0 
            root = self.xmlTree.getroot()
            
            # 提取模板参数列表
            self.param_list = XmlReader.walkNode(self, root)
            
            # 是否替换原有模板
            if self.pos == self.cnt: # 原模板已经模板化了，不需要再次保存
                pass
            else:  
                self.write_xml(self.curFilepath)
            
            # 返回数据
            s = ET.tostring(root, encoding="utf-8", method="xml")
            s = s.replace('\n','').replace('\r','').replace(' ','').replace('\t','') #替换换行、空白等字符
            return (s, self.param_list)
    
    """=========================================================
    函数名称: find_node_list
    功能描述: 根据xpath获取节点列表 
    参数列表: xpath——xpath路径
    返回结果: xml节点列表       
    ============================================================""" 
    def find_node_list(self, xpath):  
        return self.xmlTree.findall(xpath)
    
    """=========================================================
    函数名称: get_node_by_kv_map
    功能描述: 根据xpath获取节点列表 
    参数列表: node_list——节点列表; kv_map: 匹配属性信息
    返回结果: 节点   
    ============================================================""" 
    def get_node_by_kv_map(self, node_list, kv_map):
        for node in node_list:
            for key, value in kv_map.items():  
                if node.get(key) == value:
                    return node 
                else:
                    pass

    """=========================================================
    函数名称: get_desc_by_xpath
    功能描述: 根据xpath以及属性信息提取Desc属性    
    参数列表: xpath——xpath路径, em——错误模块, ec——错误码
    返回结果: (错误模块描述, 错误码描述)       
    ============================================================"""  
    def get_desc_by_xpath(self, xpath, em, ec):
        em_desc, ec_desc = u'未找到错误模块', u'未找到错误码'
        try:
            # 查找错误模块信息
            node_list   = self.find_node_list(xpath)
            found_node  = self.get_node_by_kv_map(node_list, {'Value':em})
            em_desc     = found_node.get('Desc')
            component   = found_node.get('Component')
            
            # 查找错误码信息
            node_list   = self.find_node_list('ErrorCode')
            found_node  = self.get_node_by_kv_map(node_list, {'Component': component})
            node_list   = found_node.getchildren()
            for node in node_list:
                if node.get('Value') == ec:
                    ec_desc = node.get('Desc')
                    break
                else:
                    pass
        except:
            traceback.print_exc()
            
        return (em_desc, ec_desc)