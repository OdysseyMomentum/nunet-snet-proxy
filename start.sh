#!/bin/bash

# Script to start snet-proxy

BASE_DIR=$(readlink -f $(dirname ${BASH_SOURCE[0]}))

C_NAME=''

I_NAME_PROXY="snet_proxy"
C_NAME_PROXY="snet_proxy"

INFURA="https://ropsten.infura.io/v3/1e7ce8503f6c42bba499fde740512644"


build_proxy() {
    docker build --build-arg INFURA=$INFURA  -t $I_NAME_PROXY $BASE_DIR -f Dockerfile
}

run_proxy() {
    docker run -i --name $C_NAME_PROXY -p 7005:7005 -v /home/$USER/snet-proxy:/snet-proxy $I_NAME_PROXY
    C_NAME=$C_NAME_PROXY
}

stop_service() {
    docker stop $C_NAME
}

help () {
    echo "Usage: bash start.sh OPTION [LABEL] "
    echo "  Options:"
    echo "    build-proxy        build the proxy docker image "
    echo "    run-proxy        run the snet proxy"

    echo "    stop         stop the snet proxy (stop container)"
    echo -e "\n  LABEL  :  image and container label (optional - default=snet-proxy)"

}

case $1 in
  build-proxy)build_proxy ;;
  run-proxy) run_proxy ;;

  stop) stop_service ;;
  *) help ;;
esac
