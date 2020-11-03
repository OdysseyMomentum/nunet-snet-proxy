# Dockerfile - to build the snet-proxy api

FROM python:3.7

COPY . /SNET-PROXY 
WORKDIR /SNET-PROXY

RUN pip3 install -r requirements.txt

EXPOSE 7000

CMD ["python3", "app.py"]