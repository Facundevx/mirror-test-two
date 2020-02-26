FROM python:3.7-slim-stretch

RUN apt-get update && apt-get -y install git

RUN git clone -b master https://github.com/Facundevx/learning_log.git

EXPOSE 8000

WORKDIR /learning_log

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN mkdir /log

ENV GUNICORN_CMD_ARGS="--bind=:8000 --workers=4"

CMD ["gunicorn", "app:app"]

