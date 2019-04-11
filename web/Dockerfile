#todo: user - run not as root
FROM python:3.6-slim
#RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

COPY /app/requirements.txt /requirements.txt

RUN apt-get update && \
    apt-get install -y build-essential python3-dev libevent-dev gcc && \
    pip install --upgrade pip

RUN pip3 install -r /requirements.txt
RUN ["mkdir", "-p", "/app"]
COPY /app /app
COPY ./init_system.sh /init_system.sh
RUN ["chmod", "+x", "/init_system.sh"]
CMD ["gunicorn", "--chdir", "/app", "--bind", ":8000", "main_portal.wsgi:application"]
