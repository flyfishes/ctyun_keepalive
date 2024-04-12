# ctyun_keepalive
天翼云电脑自动连接保活，阻止休眠

#2运行条件：
 python 3以上版本

 #2运行方法：
 1. 安装python3
    Windows直接官网下载安装。
    linux（centos） 可以用 yum install python3
    linux（其他）  可以用apt get python3
     
 2. 安装python库
pip3 install  -r requirements.txt

3. 安装浏览器chromedriver 或者edgedriver
   chrome 访问这里下载，
   https://getwebdriver.com/chromedriver#stable
   edge浏览器访问这里下载
   https://developer.microsoft.com/zh-cn/microsoft-edge/tools/webdriver/?form=MA13LH

4. 运行程序
   python ctyun-alive.py 手机号 天翼云密码

5.  运行结果：
  可以查看日志文件ctyun.log
  可以查看截图ctyun.png

#2注意
支持chrome浏览器，edge浏览器，包括界面方式和无界面方式

#2可能错误
1. 多次密码输入，会出现验证码提示。
  
