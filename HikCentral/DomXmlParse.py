# coding: utf-8

"""==================================================================
Copyright(c) 2015-2016 Hangzhou Hikvision Digital Technology Co.,Ltd
文件名称:  DomXmlParse.py
简要描述： 利用python标准库dom解析xml
作    者： Qiu Jiangping 
完成日期:  2017-9-13
修订说明: 
=================================================================="""

import traceback
import xml.dom.minidom

class DomXmlParse:  
    """=========================================================
    函数名称: __init__
    功能描述: 初始化解析xml文件
    参数列表: xmlParam——xml路径或xml文本, mode——xml是文本还是内容的标记        
    返回结果:                  
    ============================================================"""  
    def __init__(self, xmlParam, mode=False):
        if mode: # xmlFile为文本
            try:
                self.dom = xml.dom.minidom.parseString(xmlParam)
            except:
                self.dom = xml.dom.minidom.parseString('<ErrorInfo><error_info>Expect data is not defined or abnoraml</error_info></ErrorInfo>')
        else: # xmlFile为文件
            self.dom = xml.dom.minidom.parse(xmlParam)
        
        # 提取根节点
        self.root = self.dom.documentElement

    """=========================================================
    函数名称: walkNode
    功能描述: 遍历节点，提取有数值的节点的数值与xpath
    参数列表: node——需要遍历的节点,默认为根节点    
    返回结果: 无         
    ============================================================"""                
    def walkNode(self, node):
        if node != None:
            node_list = node.childNodes
            node_count = len(node_list)
            
            if node_count == 0:
                node_tag   = str(node.nodeName)
                node_value = str(node.nodeValue)
                if '\n' not in node_value and node_value != None:
                    self.xpath_list.append(self.get_node_xpath(node))
                    self.value_list.append(node_value)
            
            for child in node_list:
                DomXmlParse.walkNode(self, child)
                
    """=========================================================
    函数名称: get_node_xpath
    功能描述: 根据node节点提取其xpath
    参数列表: node——节点；    
    返回结果: 无         
    ============================================================"""  
    def get_node_xpath(self, node):
        self.temp_xpath_list = []
        while node != None:
            node_name = str(node.nodeName)
            node = node.parentNode
            if ('#text' == node_name or '#document' == node_name):
                continue
            else:
                self.temp_xpath_list.append(node_name)

        # 清除根节点字段
        self.temp_xpath_list.pop()
        self.temp_xpath_list = reversed(self.temp_xpath_list)
        return '/'.join(self.temp_xpath_list)
    
    """=========================================================
    函数名称: rename_same_xpath
    功能描述: 重命名列表中xpath相同的元素   
    返回结果: 无         
    ============================================================""" 
    def rename_same_xpath(self):
        for xpath in self.xpath_list:
            new_listt = [m for (m, n) in enumerate(self.xpath_list) if n == xpath]
            cnt = self.xpath_list.count(xpath)
            if cnt > 1:
                for (m,n) in enumerate(new_listt):
                    value = self.xpath_list[n]
                    self.xpath_list[n] = value + '[%s]'%str(m)
            else:
                pass
            
    """=========================================================
    函数名称: get_xpath_value_dict
    功能描述: 获取xpath:value字典
    返回结果: 无         
    ============================================================"""
    def get_xpath_value_dict(self):
        self.temp_xpath_list = []
        self.xpath_list  = []
        self.value_list  = []
        self.walkNode(self.root)
        self.rename_same_xpath()
        return dict(zip(self.xpath_list, self.value_list))