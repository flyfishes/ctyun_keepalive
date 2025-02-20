# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
# ActionChains(driver).key_down(Keys.CONTROL).click(lnk).key_up(Keys.CONTROL).perform()
from pyvirtualdisplay import Display
import time
import logger
import logging
import sys,os
import json
import requests
import threading
from queue import Queue
import my_captcha

import webthread

__g_logger = logger.Logger(path="static/ctyun.txt",Flevel=logging.INFO)

def isNeedDisplay(bMustVirtualDisplay=1):
    if (r"linux" in sys.platform):
        if (bMustVirtualDisplay):
            return 1
        else:
            return 2
    return 2


def pushmsg(push_token,title,content):
    if(push_token==''):return ''
    url='https://iyuu.cn/'+push_token+'.send?text=%s&desp=%s'%(title,content)
        
    data = {
            "token":push_token,
            "title":title,
            "content":content
        }    
    body=json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type':'application/json'}
    ret=requests.post(url,data=body,headers=headers)
    return ret.text


def keepalive_ctyun2(parms,url="https://pc.ctyun.cn/#/login"):
    __g_logger.setModulename("keepalive_ctyun")
    if (parms is None):
        __g_logger.warning("Wrong parameters parms")
        return -1
        
    ctyun_steps=[{"name":"login Input","elems":[['account',By.CLASS_NAME,'send_keys','%ACCOUNT%'],
                                               ['password',By.CLASS_NAME,'send_keys','%CTPASSWORD%'],
                                               ['btn-submit',By.CLASS_NAME,'click','3']]}
                ,{"name":"Enter YunMachine","elems":[['desktop-main-entry',By.CLASS_NAME,'click','5']]}
                ,{"name":"Windows login","elems":[[ "close-ai", "class name", "click", "3" ],
                                                ['screenContainer',By.CLASS_NAME,'click','15'],
                                                 ['winpassword',"active_element",'send_keys','%WINPASSWORD%']]}
                ]
    for step in ctyun_steps:
        for elem in step['elems']:
            if(elem[3] =="%ACCOUNT%"):
                elem[3]=parms['account']
            elif(elem[3] =="%CTPASSWORD%"):
                elem[3]=parms['password']
            elif(elem[3] =="%WINPASSWORD%"):
                elem[3]='999'+parms['password']
    #print(ctyun_steps)
            
    if(parms['browserType'] =='edge'):
        options = webdriver.EdgeOptions() #ChromeOptions()
        options.use_chromium=True
    else:
        options = webdriver.ChromeOptions()
        
    isDisplay =  isNeedDisplay()
    if (isDisplay==1):
        display = Display(visible=False, size=(480, 600))
        display.start()
        options.add_argument('excludeSwitches=enable-automation')
        options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    elif(isDisplay==2): #normal Linux none-interface mode
        options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
        options.add_argument('window-size=800x600')  # 指定浏览器分辨率
        options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        options.add_argument('blink-settings=imagesEnabled=true')  # 不加载图片, 提升速度
        options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    else:
        options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    options.add_argument('permissions.default.stylesheet=2')    #不用网站提供的css
    options.add_argument('--enable-chrome-browser-cloud-management')

    if(parms['listen_url'] == ''): listen_url=getDefaultUrl(port=parms['listenport'])
    listen_url=f'<a href="{listen_url}">点击输入(click to input)</a>'

    try:
        if(parms['listenport']>0):
            verifyCodeQueue=Queue()
            webthread.web_run(verifyCodeQueue,port=parms['listenport'])   #拉起一个web监听线程，便于输入验证码

        __g_logger.info("try start selenium")
        if(parms['browserType'] =='edge'):
            options.binary_location='C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe' if (parms['browserPath']=='') else parms['browserPath']
            driver = webdriver.Edge(options=options)
        else:
            options.binary_location='D:\programs\chrome\chrome.exe' if (parms['browserPath']=='') else parms['browserPath']
            driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)
        
        i=0
        bFoundVercode=False
        while i<len(ctyun_steps):
            step= ctyun_steps[i]
            __g_logger.info("step" + str(i+1) + ":"+ step['name']+",Now url:" +driver.current_url)

            if(driver.current_url == url):  #当前为登录页面，需要额外判断是否需要输入验证码
                try:
                    obj = driver.find_element(By.CLASS_NAME,'code')
                    objimg = driver.find_element(By.CLASS_NAME,'code-img')
                    if(obj.get_attribute('value')==''):
                        __g_logger.warn("登录需要验证码!" + objimg.get_attribute('src') )
                        pushmsg(parms['push_token'],'天翼云电脑保活需要验证码', listen_url)
                        driver.get_screenshot_as_file('static/ctyun.png')
                        objimg.screenshot("static/verifyCode.png")
                        bFoundVercode=True
                        if(parms['listenport']>0):
                            try:
                                verifyCode=my_captcha.captcha_pic('static/verifyCode.png')
                                if(verifyCode==None):
                                    verifyCode= verifyCodeQueue.get(block=True,timeout=60)
                                __g_logger.info('收到/识别验证码:'+verifyCode)
                            except Exception:
                                __g_logger.warn("获取验证码超时(60s)")
                                pass
                        else:
                            verifyCode=input('请输入验证码:')
                        obj.clear()
                        obj.send_keys(verifyCode)
                        if(i>0):    #如果要出现输入验证码，退回上一步重新登录页面操作
                            i=i-1
                            continue
                except NoSuchElementException as e:
                    pass
            
            for elem in step['elems']:
                if(elem[1] == 'active_element'):
                    __g_logger.debug(f"send active_element keys:{elem[3]}")
                    driver.switch_to.active_element.send_keys(elem[3]);
                    driver.switch_to.active_element.send_keys(Keys.ENTER);
                else:
                    try:
                        obj = driver.find_element(elem[1],elem[0])
                        if(obj):
                            __g_logger.debug(f"find {elem[0]}={elem[3]}")
                            if (elem[2]=='send_keys'):
                                obj.clear()
                                obj.send_keys( elem[3])
                            elif (elem[2]=='click'):
                                obj.click()
                                if(len(elem[3])>0): time.sleep(int(elem[3]))    #最后一步登录唤醒可能等待时间较长
                    except NoSuchElementException as e:
                        __g_logger.warn("element not found:" + elem[0] )
                        try:
                            tips_obj=driver.find_element(By.CLASS_NAME,'el-message__content')
                            __g_logger.warn("tips:"+tips_obj.text)
                        except NoSuchElementException as e:
                            pass
                        
                        #return -2
            i=i+1
        #end while step                

        time.sleep(15)
        
    except Exception as e:
        import traceback
        __g_logger.error( traceback.format_exc() )
    finally:    #即使中间有return代码也会执行
        driver.get_screenshot_as_file('static/ctyun.png')
        __g_logger.info("save to static/ctyun.png")
        driver.quit()

    if (isNeedDisplay()==1):
        display.stop()
    pushmsg(parms['push_token'],'天翼云电脑保活成功',time.asctime())
    return 0

#获取输入验证码网页地址
# 参数：
#   protocal:http或https
#   port端口
#   iptype：local（局域网地址），internet（互联网地址）
def getDefaultUrl(protocal='http',port=8000,iptype='local'):
    ip=None
    if(iptype == 'local'):
        #局域网
        try:
            import socket
            host_name = socket.gethostname()
            ip = socket.gethostbyname(host_name)
        except:
            __g_logger.warn("Can not get local IP")
    else:
        #互联网    
        ip=requests.get('http://ip-api.com/csv/?fields=query', timeout=5).text
    #listen_url='<a href="http://'+ip.rstrip()+':8000/">click to input.</a>'
    listen_url=f'{protocal}://{ip}:{port}/'
    return listen_url

# chromedriver 下载
# https://getwebdriver.com/chromedriver#stable
#
                
if __name__ == '__main__':
    #my.json默认参数    
    parms=\
        {  'account':'',        #你的天翼云账号,必输项
           'password':'',       #你的天翼云电脑密码,必输项（用"")
           'browserType':'edge',  #edge或者chrome
           'browserPath':'',      #本机edge或chrome浏览器安装路径，默认不需要提供
           'listenport':8000,     #如果=0，则默认键盘输入    
           'listen_url':'',       #监听输入验证码网站地址http://ip:listenport/path,默认为当前局域网http://ip:8000/
           'push_token':'',       #微信推送，https://iyuu.cn免费申请token
        }
    
    try:
        with open(r"my.json",encoding='utf-8') as json_file:
            parms = json.load(json_file)
            if ('browserType' not in parms):parms['browserType']='edge'
            if ('browserPath' not in parms):parms['browserPath']=''
            if ('listenport'  not in parms):parms['listenport']=8000
            if ('listen_url'  not in parms):parms['listen_url']=''
            if ('push_token'  not in parms):parms['push_token']=''
    except:
        __g_logger.warn("未发现my.json配置文件，或配置文件格式有误。")

    if (len(sys.argv) >= 3 ):
        parms['account'] = sys.argv[1]
        parms['password']= sys.argv[2]
        
        if(len(sys.argv) > 3):
            parms['browserType']=sys.argv[3]
        if(len(sys.argv) > 4 and len(sys.argv[4])>=8 ):
            parms['browserPath']=sys.argv[4]          
        if(len(sys.argv) > 5):
            parms['listenport']=sys.argv[5]                        
    elif(parms['account']==''  or  parms['password']==''):
        print('Usage: python ctyun-alive.py <account> <"password"> [edge] [edge_path] [listenport]')
        sys.exit(1)
        
    print(parms)
             
    ret=keepalive_ctyun2(parms=parms)
    
