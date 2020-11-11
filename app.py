# app.py - a flask api using flask_restful 
from flask import Flask, request, jsonify
from flask_cors import CORS

from utils import *

import json

import uclnlp_service_pb2_grpc as pb2_grpc
import uclnlp_service_pb2 as pb2

from config import config, rpc_endpoints

app = Flask(__name__)
CORS(app) # to enable CORS for the routes, unless from the front end response becomes Network Error

@app.before_first_request
def set_account():
    subprocess.run([ "snet","identity","create","uclnlp-service","key","--private-key",
                    config['private_key']])
    subprocess.run(["snet","network","ropsten"])
    subprocess.run(["snet","identity","uclnlp-service"])


@app.route('/get_score', methods=['GET'])
def get_score():
    url = request.args.get('url')
    req = pb2.InputData(headline=headline, body=body)
    proc = "stance_classify"
    result = utils.call_sdk(req, proc)
    return str(result)

proxy_port = 7005
org_id = "odyssey-org"
service_id = "uclnlp-service"
group_name = "default-group"
#config['eth_rpc_endpoint'] rpc_endpoints[0]
utils = utils(org_id, service_id, group_name, rpc_endpoints, proxy_port)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=proxy_port)