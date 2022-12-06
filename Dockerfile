FROM registry.cn-shanghai.aliyuncs.com/devcon/spiderdev:v2.1
ADD . /app
WORKDIR /app
RUN mkdir /app/log
RUN python3 -m pip install flask -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN python3 -m pip install flask_cors -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN python3 -m pip install qqwry-py3 -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN python3 -m pip install waitress -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]