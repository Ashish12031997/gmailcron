FROM python:3.12

WORKDIR /gmail_api
# COPY ./logs/info.log /logs/info.log
# COPY ./logs/error.log /logs/error.log
COPY . /gmail_api
RUN mkdir -p logs
RUN mkdir -p celery_logs
RUN mkdir -p beat_log
RUN chmod +x start-server.sh
RUN if [ -d "runscripts" ] && [ "$(ls -A runscripts)" ]; then chmod +x runscripts/*; fi
# # RUN chmod -R 777 /logs
# COPY . /gmail_api
# # # install dependencies
# RUN apt-get update -y \
#     && apt-get install -y  supervisor
# # copy and install requirements
RUN apt-get update -y && apt-get install -y \
    postgresql-client \
    libpq-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8000
STOPSIGNAL SIGTERM
CMD ["/gmail_api/start-server.sh"]
