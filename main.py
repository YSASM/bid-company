#!/usr/bin/python3
# encoding:utf-8
import json,logging,hashlib,os,datetime,base64
from logging import handlers
import waitress
from time import time,sleep,strftime,localtime
import traceback
from flask import Flask, render_template, request, jsonify,session,redirect,url_for,make_response
from flask_cors import *
from service import service
from config import Config
from api.mode import Detail,List
from model.bid_admin import AdminDao,Admin
from model.bid_company_log import CompanyLogDao
from base.ansync_call import async_call
from service.message import MessageService
# from qqwry import updateQQwry
# result = updateQQwry('base/qqwry.dat')
logintoken = []
logger = logging.getLogger()
for h in logger.handlers:
    logger.removeHandler(h)
fmt = "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
file_handler = handlers.TimedRotatingFileHandler(
    filename="log/api.log", when="D", interval=1, backupCount=14
)
file_handler.setFormatter(logging.Formatter(fmt))
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
if Config.env() == "test" or Config.env() == "dev":
    console_handler.setLevel(logging.DEBUG)
else:
    console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(logging.Formatter(fmt))
logger.addHandler(console_handler)
def del_log_run(day):
    ms = MessageService()
    cl = CompanyLogDao()
    logger.info("【del_log】开始清理")
    t = int(time())-(day*86400)
    cl.del_old(t)
    logger.info('【del_log】删除了company_log%s前的日志' % str(strftime("%Y-%m-%d %H:%M:%S", localtime(t))))
    ms.send_text('【del_log】删除了company_log%s前的日志' % str(strftime("%Y-%m-%d %H:%M:%S", localtime(t))))
api = Flask(__name__) 
api.config['SECRET_KEY']=os.urandom(24)
# session.permanent=True
api.config['PERMANENT_SESSION_LIFETIME']=datetime.timedelta(days=7)
CORS(api, supports_credentials=True, resources=r"/*")
@async_call
def del_log(day=7):
    daycount = 86400
    while True:
        if daycount>=86400:
            del_log_run(day)
            daycount=0
        sleep(1)
        daycount+=1
    
    
def run_api():
    main = Main()
    del_log()
    # main.api.run(port=9252,host='0.0.0.0') # 启动服务
    waitress.serve(api, host='0.0.0.0', port='9258')# 启动服务
class Main(object):
    ad = AdminDao()
    s = service.Service()
    def make_token(username,password,ip):
        return hashlib.md5(username.encode("utf-8")).hexdigest()+'-'+hashlib.md5(password.encode("utf-8")).hexdigest()+'-'+hashlib.md5(ip.encode("utf-8")).hexdigest()
    def decode_base64(data):
        data = data.encode("utf-8")
        missing_padding = 4 - len(data) % 4
        if missing_padding:
            data += b'=' * missing_padding
        return base64.decodebytes(data)
    def isLogin(ip,t,token=None):
        global logintoken
        username = session.get('username')
        password = session.get('password')
        if token:
            for lt in logintoken:
                if token == lt[0]:
                    if t-lt[1]>86400:
                        logintoken.pop(logintoken.index(lt))
                        return False
                    lt[1] = t
                    return token
        if not username or not password:
            return False
        token = Main.make_token(username,password,ip)
        if Main.ad.login(username,password):
            logintoken.append([token,t])
            return token
        return False
    @api.route("/loginout",methods=["POST"])
    def loginout():
        session.clear()
        return redirect(url_for('manage'))
    @api.route("/login",methods=["POST","GET"])
    def login():
        if request.method=='POST':
            session['username']=request.form['username']
            session['password']=request.form['password']
            return redirect(url_for('manage'))
        return render_template('login.html')
    @api.route('/manage',methods=['get'])
    def manage():
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        token = request.cookies.get('session')
        if token:
            token = token.split('.')
            token = Main.decode_base64(token[0])
            token = json.loads(token)
            token = Main.make_token(token['username'],token['password'],ip)
        token = Main.isLogin(ip,time(),token=token)
        if token:
            res = make_response(redirect(url_for('manageonoff')))
            return res
        return redirect(url_for('login'))
    
    @api.route('/managestatistics',methods=['get']) 
    def managestatistics():
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        token =request.cookies.get('session')
        if token:
            token = token.split('.')
            token = Main.decode_base64(token[0])
            token = json.loads(token)
            token = Main.make_token(token['username'],token['password'],ip)
        token = Main.isLogin(ip,time(),token=token)
        if token:
            res = make_response(render_template('statistics.html',username=session['username'],avatar=Main.ad.get_avatar(session['username'],session['password'])))
            return res
        return redirect(url_for('login'))

    @api.route('/managelog',methods=['get']) 
    def managelog():
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        token =request.cookies.get('session')
        if token:
            token = token.split('.')
            token = Main.decode_base64(token[0])
            token = json.loads(token)
            token = Main.make_token(token['username'],token['password'],ip)
        token = Main.isLogin(ip,time(),token=token)
        if token:
            res = make_response(render_template('log.html',username=session['username'],avatar=Main.ad.get_avatar(session['username'],session['password'])))
            return res
        return redirect(url_for('login'))
    
    @api.route('/manageonoff',methods=['get']) 
    def manageonoff():
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        token =request.cookies.get('session')
        if token:
            token = token.split('.')
            token = Main.decode_base64(token[0])
            token = json.loads(token)
            token = Main.make_token(token['username'],token['password'],ip)
        token = Main.isLogin(ip,time(),token=token)
        if token:
            res = make_response(render_template('onoff.html',username=session['username'],avatar=Main.ad.get_avatar(session['username'],session['password'])))
            return res
        return redirect(url_for('login'))
if __name__ == '__main__':
    run_api()