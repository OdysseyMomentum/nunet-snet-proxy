from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

from extract import *
from snet import sdk
from config import config, rpc_endpoints

import uclnlp_service_pb2
import uclnlp_service_pb2_grpc

import athenefnc_pb2
import athenefnc_pb2_grpc

import fake_news_score_pb2
import fake_news_score_pb2_grpc

service=""
#service = "uclnlp"

snet_sdk = sdk.SnetSDK(config)
org_id='odyssey-org'
if service == "uclnlp":
        service_id='uclnlp-service'
        service_client = snet_sdk.create_service_client(
                org_id,
                service_id,
                uclnlp_service_pb2_grpc.UCLNLPStanceClassificationStub,
                group_name='default_group',
                concurrent_calls=10)

elif service == "athene":
       service_id='athene-service'
        service_client = snet_sdk.create_service_client(
                org_id,
                service_id,
                athenefnc_pb2_grpc.AtheneStanceClassificationStub,
                group_name='default_group',
                concurrent_calls=10)
else :
        service_id='fakenews-service'
        service_client = snet_sdk.create_service_client(
                org_id,
                service_id,
                fake_news_score_pb2_grpc.FakeNewsScoreStub,
                group_name='default_group',
                concurrent_calls=10)


app = Flask(__name__)
CORS(app) # to enable CORS for the routes, unless from the front end response becomes Network Error

@app.route('/get_score', methods=['GET'])
def get_score():
   url = request.args.get('url')
   headline = extract_headline(url)
   body = extract_body(url)
   if service == "uclnlp":
           req = uclnlp_service_pb2.InputData(headline=headline, body=body)  
           result = service_client.service.stance_classify(req)
   elif service == "athene":
           req = athenefnc_pb2.InputData(headline=headline, body=body)  
           result = service_client.service.stance_classify(req)
   else :
           req = fake_news_score_pb2.InputData(headline=headline, body=body)  
           result = service_client.service.stance_classify(req)
           res = str(result).split('\n')
           res.pop(0)
           result = '\n'.join(map(str, res))
   
   return str(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7005)