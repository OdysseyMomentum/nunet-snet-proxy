# app.py - a flask api using flask_restful 
from flask import Flask, request, jsonify
from flask_cors import CORS
from numpyencoder import NumpyEncoder

from utils import *

import json

import fake_news_pb2_grpc
import fake_news_pb2

from config import config, rpc_endpoints

app = Flask(__name__)
CORS(app) # to enable CORS for the routes, unless from the front end response becomes Network Error

@app.route('/get_score', methods=['POST', 'GET'])
def get_fake_news_score():
    if request.method=='POST':
        json_value=request.get_json()
        url=json_value['url']
        request = fake_news_pb2.Input(url=url)
        proc = "getScore"
        result = utils.call_sdk(request, proc)
        return str(result)
    else:
        url = request.args.get('url')
        request = fake_news_pb2.Input(url=url)
        proc = "getScore"
        result = utils.call_sdk(request, proc)
        return str(result)

proxy_port = 7005
org_id = "odyssey-org"
service_id = "snet-proxy"
group_name = "default-group"
config['eth_rpc_endpoint'] rpc_endpoints[0]
utils = utils(org_id, service_id, group_name, rpc_endpoints, proxy_port)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=proxy_port)