FROM python:3.7-slim-stretch

RUN git remote master https://github.com/Facundevx/learning_log
RUN git clone -b master https://github.com/Facundevx/learning_log

EXPOSE 8000

WORKDIR /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV GUNICORN_CMD_ARGS="--bind=:8000 --workers=4"

CMD ["gunicorn", "app:app"]

