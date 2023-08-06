#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ConfigParser
import os
from txInterface import basic, getValue
from txInterface.log import logger


#获取配置文件节点的名称
def getPath(wpath,name):
    proDir = '/home/tx-deepocean/Downloads/autotest'
    try:
        path = os.path.join(proDir, "test_data", 'config.ini')
        cf = basic.getconfig(path)
        value = cf.get(wpath, name)
    except Exception as e:
        return "fail"
    excel_path = os.path.join(proDir, "test_data", value)
    return excel_path
#获取请求的ip\port
def getiport(wpath,name):
    result = getPath(wpath,name)
    params = result.split("/")
    logger.info(params[params.__len__()-1])
    return params[params.__len__()-1]
#获取返回的过滤值
def getTarget(wpath,name):
    proDir = '/home/tx-deepocean/Downloads/autotest'
    path = os.path.join(proDir, "test_data", 'config.ini')
    cf = basic.getconfig(path)
    value = cf.get(wpath, name)
    return value

#获取配置文件的路径
def dirpath():
    proDir = '/home/tx-deepocean/Downloads/autotest'
    path = os.path.join(proDir, "test_data", 'config.ini')
    return path
#生成配置文件数据
def modifyValues(ip, port, target, list):
    path = dirpath()
    fixConfig = ConfigParser.ConfigParser()
    fixConfig.add_section("message")
    fixConfig.set("message", "ip", ip)
    fixConfig.set("message", "port", port)
    fixConfig.add_section("target")
    fixConfig.set("target", "target", target)
    for param in list:
        fixConfig.add_section(param)
        fixConfig.set(param, "text_name", param+".txt")
    fixConfig.write(open(path, "wb"))
    return "sucess"
#拿出配置文件txt脚本数据
def getFileName():
    proDir = '/home/tx-deepocean/Downloads/autotest'
    params =[]
    path = dirpath();
    fixConfig = ConfigParser.ConfigParser()
    fixConfig.read(path)
    sections = fixConfig.sections()
    print sections
    for section in sections:
        items = fixConfig.items(section)
        for param in items:
            if param.__contains__("ip") or param.__contains__("port") or param.__contains__("target"):
                continue
            else:
                excel_path = os.path.join(proDir, "test_data", param[1])
                params.append(excel_path)
    logger.info("The parameters we get are")
    logger.info(params)
    return params
#获取要执行的case数据
def getCaseValue():
    list = []
    logcase = []
    result = getFileName()
    for param in result:
      res = getValue.get_txt_value(param)
      logcase.append(res)
    for param in logcase:
        for re in param:
            list.append(re)
    return list
#获取上个接口的返回参数
def  getLastValue(returnValue,lastValue):
    changeValue = ""
    for param in returnValue:
        params = param.split(".")
        for retval in params:
            if lastValue == retval:
                changeValue = params[len(params) - 1]
    return changeValue

#对返回数据进行过滤
def getRes(set, list):
    retur = list.replace('[', "").replace(']',"").replace("'","").split(",")
    result = []
    for param in set:
        count = 0
        for ll in retur:
            if param.__contains__(ll.strip()):
                count = count + 1
            else:
                continue
        if count == 0:
            rest = param.encode('gbk')
            result.append(rest)
        else:
            set.remove(param)
            return getRes(set, list)
    return result
if __name__ == '__main__':
    modifyValues()