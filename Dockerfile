
FROM python:3.8
EXPOSE 8080

VOLUME /data/
VOLUME /conf/
VOLUME /static/


RUN apt-get update && \
    apt-get install -y \
                    vim \
                    supervisor \
                    dumb-init

COPY . /usr/src/app
WORKDIR /usr/src/app

COPY project/local_settings.sample.py project/local_settings.py
COPY supervisor/supervisord.conf /etc/supervisor/supervisord.conf
COPY supervisor/prod.conf /etc/supervisor/conf.d/sms-service.conf

RUN pip install pip==20.2.4
ADD requirements.txt .
RUN pip install -r requirements.txt

CMD test "$(ls /conf/local_settings.py)" || cp project/local_settings.py /conf/local_settings.py; \
    rm project/local_settings.py; ln -s /conf/local_settings.py project/local_settings.py; \
    rm -rf static; ln -s /static static; \
    python3 ./manage.py migrate; \
    python3 ./manage.py collectstatic --noinput; \
    /usr/bin/supervisord