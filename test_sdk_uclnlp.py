from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from extract import *
from snet import sdk
import uclnlp_service_pb2 as pb2
import uclnlp_service_pb2_grpc as pb2_grpc

from config import config, rpc_endpoints

snet_sdk = sdk.SnetSDK(config)
org_id='odyssey-org'
service_id='uclnlp-service'
service_client = snet_sdk.create_service_client(
        org_id,
        service_id,
        pb2_grpc.UCLNLPStanceClassificationStub,
        group_name='default_group',
        concurrent_calls=1)

app = Flask(__name__)
CORS(app) # to enable CORS for the routes, unless from the front end response becomes Network Error

@app.route('/get_score', methods=['GET'])
def get_score():
   url = request.args.get('url')
   headline = extract_headline(url)
   body = extract_body(url)
   req = pb2.InputData(headline=headline, body=body)
   result = service_client.service.stance_classify(req)
   return str(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7005)