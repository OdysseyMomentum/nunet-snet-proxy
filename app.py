# app.py - a flask api using flask_restful 
from flask import Flask, request, jsonify
from flask_cors import CORS

from utils import *

import json

import rfakenews_service_pb2_grpc as pb2_grpc
import rfakenews_service_pb2 as pb2

from config import config, rpc_endpoints

app = Flask(__name__)
CORS(app) # to enable CORS for the routes, unless from the front end response becomes Network Error

@app.before_first_request
def set_account():
    subprocess.run([ "snet","identity","create","rfakenews-service","key","--private-key",
                    config['private_key']])
    subprocess.run(["snet","network","ropsten"])
    subprocess.run(["snet","identity","rfakenews-service"])


@app.route('/get_score', methods=['POST', 'GET'])
def get_score():
    if request.method=='POST':
        json_value=request.get_json()
        url=json_value['url']
        request = pb2.InputFNS(url=url)
        proc = "getScore"
        result = utils.call_sdk(request, proc)
        return str(result)
    else:
        url = request.args.get('url')
        request = pb2.InputFNS(headline="agjag", body="djaga")
        proc = "fn_score_calc"
        result = utils.call_sdk(request, proc)
        return str(result)

proxy_port = 7005
org_id = "odyssey-org"
service_id = "rfakenews-service"
group_name = "default-group"
#config['eth_rpc_endpoint'] rpc_endpoints[0]
utils = utils(org_id, service_id, group_name, rpc_endpoints, proxy_port)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=proxy_port)