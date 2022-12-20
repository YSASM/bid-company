FROM registry.cn-shanghai.aliyuncs.com/devcon/spiderdev:v3.0
ADD . /app
WORKDIR /app
RUN mkdir /app/log
RUN chmod +x /app/start.sh
RUN chmod +x /app/status.sh
RUN chmod +x /app/api_restart.sh
RUN chmod +x /app/api_getid_restart.sh
EXPOSE 9252
CMD ["/app/start.sh"]