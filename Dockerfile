FROM registry.cn-shanghai.aliyuncs.com/devcon/companydev:v1.0
ADD . /app
WORKDIR /app
RUN mkdir /app/log
RUN chmod +x /app/start.sh
# CMD ["/app/start.sh"]