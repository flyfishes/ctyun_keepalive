#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging, os,traceback
import sys,inspect

global g_LOGGER__defaultlogfile,g_LOGGER__
g_LOGGER__defaultlogfile='ctyun.log'
g_LOGGER__ = None

class Logger:
    def __init__(self, path="", clevel=logging.INFO, Flevel=logging.DEBUG):
        global g_LOGGER__defaultlogfile,g_LOGGER__
        if (g_LOGGER__ is None):
            if path =="":
                path=g_LOGGER__defaultlogfile
            self.logger = logging.getLogger(path)
            self.logger.setLevel(logging.DEBUG)
            fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s][:%(lineno)d] %(message)s', '%Y-%m-%d %H:%M:%S')
            # 设置CMD日志
            sh = logging.StreamHandler()
            #sh.setFormatter(fmt)
            sh.setLevel(clevel)
            # 设置文件日志
            fh = logging.FileHandler(path)
            fh.setFormatter(fmt)
            fh.setLevel(Flevel)
            self.logger.addHandler(sh)
            self.logger.addHandler(fh)
            self.modulename=""
            g_LOGGER__= self
        else:
            self.logger= g_LOGGER__.logger
            self.modulename=g_LOGGER__.modulename

    def debug(self, message):
        self.logger.debug(self.modulename+message)

    def info(self, message):
        self.logger.info(self.modulename+message)

    def war(self, message):
        self.logger.warn(self.modulename+message)

    def warn(self, message):
        self.logger.warn(self.modulename+message)

    def error(self, message):
        self.logger.error(self.modulename+message)

    def cri(self, message):
        self.logger.critical(self.modulename+message)

    def exception(self, message):
        self.logger.exception(message)

    def testLogout(self, message):
        self.logger.info(self.pstack(self.modulename+message))

    def setModulename(self,modulename):
        self.modulename = "["+modulename+"]"

    def pstack(self, msg="", depth = 0):
        iLen = len(inspect.stack(0))
        if (iLen > depth and depth>0):
            iLen = depth
        i=1
        strStack=msg
        while i<iLen:
            strStack = strStack + ">>"*(i-1)
            strStack ="%s%s:%s[%d]" % (strStack,sys._getframe(i).f_code.co_filename, sys._getframe(i).f_code.co_name,sys._getframe(i).f_lineno)
            i=i+1
            if (i<iLen):
                strStack = strStack +  "\n"
        return strStack

if __name__ == '__main__':
    logyyx = Logger("", logging.INFO, logging.DEBUG)
    logyyx.setModulename('main')
    logyyx.debug('一个debug信息')
    logyyx.info('一个info信息')
    logyyx.war('一个warning信息')

    logyyx.error('一个error信息 from'+sys._getframe(1).f_code.co_name)
    logyyx.testLogout("hahaha\n")
    max_num=6
    num = int(int(max_num) / 5)
    logyyx.war("num=%d"% num)


