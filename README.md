# ctyun_keepalive
天翼云电脑自动连接保活，阻止休眠

#2运行条件：<br>
 python 3以上版本<br>

 #2运行方法：<br>
 <1>. 安装python3：<br>
    Windows直接官网下载安装。<br>
    linux（centos） 可以用 yum install python3<br>
    linux（其他）  可以用apt get python3<br>
     
 <2>. 安装python库：<br>
pip3 install  -r requirements.txt<br>

<3>. 安装浏览器chromedriver 或者edgedriver：<br>
   chrome 访问这里下载，<br>
   https://getwebdriver.com/chromedriver#stable <br>
   edge浏览器访问这里下载<br>
   https://developer.microsoft.com/zh-cn/microsoft-edge/tools/webdriver/?form=MA13LH <br>
  直接解压到当前目录下即可
 

<4>. 运行程序：<br>
   python ctyun-alive.py <手机号> <天翼云密码> [edge] [browser_exe_path] [listen_port]<br>
   注意：天翼云密码如果有(+-=等特殊字符)，请用""<br>
   edge: 浏览器名字（默认为edge，其他字符则chrome）<br>
   browser_exe_path：浏览器可执行文件路径，如果报错找不到路径，则需要指定<br>
   listen_port：web监听端口，默认不用修改8000，如果改为0，则在控制台输入验证码（阻塞模式）<br>
   可以设置自动任务，每隔半小时运行一次。<br>

<5>.  运行结果：<br>
  可以查看日志文件ctyun.log<br>
  可以查看截图static/ctyun.png<br>

#2注意：<br>
支持chrome浏览器，edge浏览器，包括界面方式和无界面方式<br>


#2可能错误：<br>
1.第一次运行会提示出现验证码，解决办法：打开微信推送，点击链接输入验证码。如果不启用微信推送，则访问地址Http://ip:8000/访问输入<br>
2. 多次错误密码输入，会出现验证码提示。<br>
  
