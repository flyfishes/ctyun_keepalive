from flask import Flask,render_template,request
from queue import Queue
import threading

app = Flask(__name__)
global __g_verifyCodeQueue

@app.route('/')
@app.route('/ctyun')
def index(name=None):
    page='''
    <html><head><title>天翼云电脑登录验证码获取</title></head>
    <meta name="viewport" content="width=device-width" initial-scale="1"/>
    <style>
     .box{
        display:-webkit-flex;
        display:flex;
        }
    </style>
    <body>
    <h2>天翼云电脑登录验证码获取</h2>
    <form action='/ctyuncode' method='POST'>
      <div class="box">请输入验证码:<input type=text name='code' maxlength=8 size=8></div>
      <input type=submit name=submit value='提交'>
      <img src='ctyun.png' border=0/>
    </form>
    </body></html>
'''
    return render_template('index.html')

@app.route('/ctyuncode',methods=['POST'])
def get_ctyuncode(name=None):
    global __g_verifyCodeQueue
    code=request.form.get('code')
    __g_verifyCodeQueue.put(code)
    print(code)

    page='''
    <html><head><title>天翼云电脑登录验证码获取结果</title></head>
    <meta name="viewport" content="width=device-width" initial-scale="1"/>
    <style>
    div{
        text-align:center;    
    >
    </style>
    <body>
    <h2>天翼云电脑登录验证码获取结果：</h2>
    <div>%s</div>
    <div><a href="/">返 回</a></div>
    </body></html>
    '''
    page=page%(code)
    return page

def web_run(q:Queue,port=8000):
    global __g_verifyCodeQueue
    __g_verifyCodeQueue=q
    server_thread = threading.Thread(target=app.run,args=('0.0.0.0',port,False,))
    server_thread.daemon = True
    server_thread.start()
    return server_thread


if __name__ == '__main__':
    __g_verifyCodeQueue=Queue()
    app.run(debug = True,host='0.0.0.0',port=8000)
    __g_verifyCodeQueue.task_done()