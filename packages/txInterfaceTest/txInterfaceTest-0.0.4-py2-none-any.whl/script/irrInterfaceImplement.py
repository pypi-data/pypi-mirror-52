#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
FileName    : test_login.py
Author      : ken
Date        : 2018-04-21
Describe    : user the paramUnittest, test login
"""
import json
import unittest
import paramunittest
from txInterface import basic, jsondiff
from txInterface.log import logger
import publicFile

#获取配置文件的ip\port\接口case数据
ip = publicFile.getiport("message", "ip")
logger.info("this  ip is  " + ip)
target = publicFile.getTarget("target", "target")
port = publicFile.getiport("message", "port")
logger.info("this is port " + port)
loginCase = publicFile.getCaseValue()
logger.info(loginCase)

#开始执行unitest,数据加载
@paramunittest.parametrized(*loginCase)
class LoginTest(unittest.TestCase):
    def setParameters(self, current_interface, last_interface, case_name, param, last_value, excepted, status):
        #参数说明
        #1.接口名称  2.上层接口名称  3.case名称  4.商城接口的参数  5.上层接口取回参数  6.预期  7.判断接口类型
        self.current_interface = current_interface
        self.last_interface = last_interface
        self.case_name = case_name
        self.param = param
        self.last_value = last_value
        self.excepted = excepted
        self.status = status
    def setUp(self):
        pass
    def test_irr_interface(self):
        res = ()
        curent = ""
        #设置case名称,放在页面说明里面
        print self.case_name
        self._testMethodDoc = self.case_name
        #判断接口的请求0为get,1为post
        if self.status == "0" or self.status =='0\n':
            logger.info(self.status)
            #判断get请求是否有上下文关系
            if self.last_interface == "${Symbol}":
                logger.info("Single Interface Testing")
                curent = self.current_interface.replace("*", self.param)
            else:
                logger.info("Upper and Lower Interface Testing")
                param = self.last_interface.replace("*", self.param)
                implement = basic.basic(ip, port)
                lastResult = implement.get(param, '')
                if lastResult.__len__() == 0:
                    self.fail("Request to return empty")
                else:
                    returnValue = jsondiff.jsonAll(lastResult)
                    if returnValue.__len__() == 0:
                        self.fail("param to return empty")
                    else:
                        lastValue = publicFile.getLastValue(returnValue, self.last_value)
                        if "" == lastValue:
                            self.fail("The return value of the previous interface is empty")
                        else:
                            curent = self.current_interface.replace("*", lastValue)
                            print curent
        implement = basic.basic(ip, port)
        result = implement.get(curent, '')
        if result.__len__() == 0:
            self.fail("Request to return empty")
        else:
            json2 = json.loads(self.excepted)
            res = jsondiff.diffKeys(result, json2, 1)
            if res.__len__() > 0:
                self.fail("key is error")
            else:
                res1 = jsondiff.diffKeys(result, json2, 2)
                logger.info("The return value is")
                logger.info(res1)
                res2 = publicFile.getRes(res1, target)
                logger.info(res2)
                if res2.__len__() > 0:
                    self.fail(res2)
                else:
                    pass
    def tearDown(self):
       pass

if __name__ == '__main__':

    unittest.main()