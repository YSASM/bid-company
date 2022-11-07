#!/usr/bin/python3
# encoding:utf-8
import json,logging
from logging import handlers
from time import time
import traceback
from flask import Flask, render_template, request, jsonify
from flask_cors import *
from service import service
from config import Config
from api.mode import Detail,List

class Main(object):
    def __init__(self):
        print(Config.get())
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


    s = service.Service()
    api = Flask(__name__) 
    CORS(api, supports_credentials=True, resources=r"/*")
    @api.route('/',methods=['get']) 
    def help():
        return render_template('help.html')
    @api.route('/manage',methods=['get']) 
    def manage():
        return render_template('manage.html')
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
    @api.route('/log',methods=['get'])
    def log():
        method = request.args.get('method')#id,time,words
        page = int(request.args.get('page'))
        limit = int(request.args.get('limit'))
        if method == 'id':
            ren = Main.s.get_log_byId(request.args.get('id'))
        elif method == 'words':
            ren = Main.s.get_log_byWords(request.args.get('words'))
        elif method == 'time':
            ren = Main.s.get_log_byTime(request.args.get('start'),request.args.get('end'))
        elif method == 'all':
            ren = Main.s.get_logs()
        pages = []
        p = []
        l = 0
        for i in ren['data']:
            if l == limit:
                pages.append(p)
                p=[]
                l=0
                continue
            p.append(i)
            l+=1
        if pages==[]:
            pages.append(p)
        ren['data']=pages[page-1]
        return jsonify(ren)
if __name__ == '__main__':
    main = Main()

    main.api.run(port=9252,debug=True,host='0.0.0.0') # 启动服务
    # ren = Main.s.get('detail','万达')