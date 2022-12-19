FROM registry.cn-shanghai.aliyuncs.com/devcon/spiderdev:v3.0
ADD . /app
WORKDIR /app
RUN mkdir /app/log
RUN chmod +x /app/start.sh
RUN chmod +x /app/status.sh
EXPOSE 9252
CMD ["/app/start.sh"]