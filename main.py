#!/usr/bin/python3
# encoding:utf-8
import json,logging,hashlib,os,datetime
from logging import handlers
from time import time
import traceback
from flask import Flask, render_template, request, jsonify,session,redirect,url_for,make_response
from flask_cors import *
from service import service
from config import Config
from api.mode import Detail,List
from model.bid_admin import AdminDao,Admin
from qqwry import updateQQwry
result = updateQQwry('base/qqwry.dat')
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
class Main(object):
    def __init__(self):
        # print(Config.get())
        pass
    ad = AdminDao()
    s = service.Service()
    api = Flask(__name__) 
    api.config['SECRET_KEY']=os.urandom(24)
    # session.permanent=True
    api.config['PERMANENT_SESSION_LIFETIME']=datetime.timedelta(days=7)
    CORS(api, supports_credentials=True, resources=r"/*")
    def isLogin(self,ip,t,token=None):
        global logintoken
        if token:
            for lt in logintoken:
                if token == lt[0]:
                    lt[1] = t
                    return token
            return False
        username = session.get('username')
        password = session.get('password')
        if not username or not password:
            return False
        token = hashlib.md5(password.encode("utf-8")).hexdigest()+'-'+hashlib.md5(password.encode("utf-8")).hexdigest()+'-'+hashlib.md5(ip.encode("utf-8")).hexdigest()
        for lt in logintoken:
            if token == lt[0]:
                lt[1] = t
                return token
        if Main.ad.login(username,password):
            logintoken.append([token,t])
            return token
        return False

    @api.route('/',methods=['get']) 
    def help():
        return render_template('help.html')
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
        ip = request.remote_addr
        token = request.headers.get('token')
        token = Main().isLogin(ip,time(),token=token)
        if token:
            res = make_response(redirect(url_for('managestatistics')))
            res.headers['token'] = token
            return res
        return redirect(url_for('login'))
    
    @api.route('/managestatistics',methods=['get']) 
    def managestatistics():
        ip = request.remote_addr
        token = request.headers.get('token')
        token = Main().isLogin(ip,time(),token=token)
        if token:
            res = make_response(render_template('statistics.html',username=session['username'],avatar=Main().ad.get_avatar(session['username'],session['password'])))
            res.headers['token'] = token
            return res
        return redirect(url_for('login'))

    @api.route('/managelog',methods=['get'],) 
    def managelog():
        ip = request.remote_addr
        token = request.headers.get('token')
        token = Main().isLogin(ip,time(),token=token)
        if token:
            res = make_response(render_template('log.html',username=session['username'],avatar=Main().ad.get_avatar(session['username'],session['password'])))
            res.headers['token'] = token
            return res
        return redirect(url_for('login'))
        
    @api.route('/list',methods=['get'])
    def list():
        start = int(float(time())*1000)
        try:
            words = request.args.get('words')
            type = request.args.get('type')
            ip = request.remote_addr
            ren = Main.s.get('list',words,ip,start,type=type)
        except:
            list = List()
            exp = traceback.format_exc()
            list.error = exp
            ren = list.bejson(list)
            Main.s.add_log(Main.s.request_time(start),ren,'list')
        return jsonify(ren)
    @api.route('/details',methods=['get'])
    def details():
        start = int(float(time())*1000)
        try:
            words = request.args.get('words')
            ip = request.remote_addr
            ren = Main.s.get('detail',words,ip,start)
        except:
            detail = Detail()
            exp = traceback.format_exc()
            detail.error = exp
            ren = detail.bejson(detail)
            Main.s.add_log(Main.s.request_time(start),ren,'detail')
        return jsonify(ren)
    def pagedown(ren,page,limit):
        pages = []
        p = []
        l = 0
        for i in ren['data']:
            p.append(i)
            l+=1
            if l == limit:
                pages.append(p)
                p=[]
                l=0
        pages.append(p)
        try:
            ren['data']=pages[page-1]
        except IndexError:
            ren['data']=[]
        return ren
    @api.route('/statistics',methods=['get'])
    def statistics():
        start = request.args.get('start')
        end = request.args.get('end')
        page = request.args.get('page')
        if page:
            page = int(page)
        limit = request.args.get('limit')
        if limit:
            limit = int(limit)
        pd = True
        method = request.args.get('method')#id,time,words
        if method == "error":
            ren = Main.s.st_error(start,end)
        elif method == "words":
            ren = Main.s.st_words(start,end)
        elif method == "time":
            pass
        elif method == "address":
            ren = Main.s.st_address(start,end)
        if page and limit and pd:
            ren = Main.pagedown(ren,page,limit)
        return jsonify(ren)
    @api.route('/log',methods=['get'])
    def log():
        method = request.args.get('method')#id,time,words
        page = request.args.get('page')
        if page:
            page = int(page)
        limit = request.args.get('limit')
        if limit:
            limit = int(limit)
        pd = True
        if method == 'id':
            ren = Main.s.get_log_byId(request.args.get('id'))
            pd = False
        elif method == 'words':
            ren = Main.s.get_log_byWords(request.args.get('words'))
        elif method == 'time':
            ren = Main.s.get_log_byTime(request.args.get('start'),request.args.get('end'))
        elif method == 'all':
            ren = Main.s.get_logs()
        if page and limit and pd:
            ren = Main.pagedown(ren,page,limit)
        return jsonify(ren)
if __name__ == '__main__':
    main = Main()

    main.api.run(port=9252,debug=True,host='0.0.0.0') # 启动服务
    # ren = Main.s.get('detail','万达')