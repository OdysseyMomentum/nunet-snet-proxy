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

@app.route('/get_score', methods=['GET'])
def get_score():
    url = request.args.get('url')
    result = utils.get_stance_classify(url)
    return str(result)

proxy_port = 7005
utils = utils()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=proxy_port)