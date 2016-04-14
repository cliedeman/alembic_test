FROM python:3.4

RUN mkdir -p /usr/app\
        && mkdir -p /usr/lib/src
WORKDIR /usr/app
COPY requirements.txt /usr/app/requirements.txt
RUN pip install -r requirements.txt --src /usr/lib/src

CMD ["python", "-m", "app"]