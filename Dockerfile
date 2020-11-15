# Dockerfile - to build the snet-proxy api

FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y \
        apt-utils \
        curl \
        wget \
        vim \
        git \
        zip \
        libudev-dev \
        libusb-1.0.0-dev \
        libxml2-dev \
        libxslt-dev \
        libjpeg-dev \
        zlib1g-dev \
        libpng-dev \
        python3.7 \
        python3-pip

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
RUN apt-get install python3.7-dev -y 
RUN pip3 install snet.sdk

RUN apt-get update
RUN wget https://github.com/fullstorydev/grpcurl/releases/download/v1.1.0/grpcurl_1.1.0_linux_x86_64.tar.gz
RUN tar -xvzf grpcurl_1.1.0_linux_x86_64.tar.gz
RUN chmod +x grpcurl
RUN mv grpcurl /usr/local/bin/grpcurl
RUN pip3 install snet-cli #( Install snet-cli)
RUN mkdir p /root/.snet && echo  \
"[network.ropsten] \n\
default_eth_rpc_endpoint = https://ropsten.infura.io/v3/1e7ce8503f6c42bba499fde740512644 \n\
default_gas_price = medium \n\
\n\
[ipfs]\n\
default_ipfs_endpoint = http://ipfs.singularitynet.io:80 \n\
\n\
[session]\n\
network = ropsten" > /root/.snet/config

COPY . /SNET-PROXY 
WORKDIR /SNET-PROXY

ENV PRIVATE_KEY="0x347e5d047b26371486f619c85378cec98027ece00fa01a0e63af71069eb50729"
ENV API_PORT=7005
#ENV SERVICE="uclnlp"
#ENV SERVICE="fakenews_nomad"
ENV SERVICE="fakenews"
ENV UCLNLP_GRPC="demo.nunet.io:7007"
ENV ATHENE_GRPC="demo.nunet.io:7008"
ENV FAKENEWS_GRPC="demo.nunet.io:7009"
ENV FAKENEWS_NOMAD_GRPC=""
ENV UCLNLP_NOMAD_GRPC=""

RUN snet identity create snet key --private-key $PRIVATE_KEY
RUN snet network ropsten
RUN snet account balance
RUN snet identity snet
RUN snet sdk generate-client-library python odyssey-org uclnlp-service
RUN snet sdk generate-client-library python odyssey-org athene-service
RUN snet sdk generate-client-library python odyssey-org fakenews-service

RUN mv ./client_libraries/odyssey-org/uclnlp-service/python/* /SNET-PROXY
RUN mv ./client_libraries/odyssey-org/athene-service/python/* /SNET-PROXY
RUN mv ./client_libraries/odyssey-org/fakenews-service/python/* /SNET-PROXY

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN pip3 install -r requirements.txt

EXPOSE $API_PORT

CMD ["gunicorn", "sdk_app:app", "--config", "./gunicorn.conf.py"]
#CMD ["gunicorn", "grpc_app:app", "--config", "./gunicorn.conf.py"]
