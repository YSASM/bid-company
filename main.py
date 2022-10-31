#!/usr/bin/python3
# encoding:utf-8
import json,logging
from logging import handlers
from flask import Flask, render_template, request
from service import service
from config import Config
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
    @api.route('/',methods=['get']) 
    def index():
        ren = {'msg':'成功访问首页','msg_code':200}
        #json.dumps 序列化时对中文默认使用的ascii编码.想输出中文需要指定ensure_ascii=False
        return json.dumps(ren,ensure_ascii=False)
    @api.route('/list',methods=['post'])
    def list():
        form = request.form
        ren = Main.s.get('list',form['words'])
        try:
            return json.dumps(ren,ensure_ascii=False)
        except:
            return {'code':'error','msg':'api Error!'}

    @api.route('/details',methods=['post'])
    def details():
        form = request.form
        ren = Main.s.get('detail',form['words'])
        return json.dumps(ren,ensure_ascii=False)
    
if __name__ == '__main__':
    main = Main()
    main.api.run(port=9252,debug=True,host='0.0.0.0') # 启动服务
    # ren = Main.s.get('detail','万达')