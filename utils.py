import subprocess
import json
import time

import uclnlp_service_pb2_grpc as pb2_grpc
import uclnlp_service_pb2 as pb2

from snet import sdk
from datetime import datetime

from config import config, rpc_endpoints


class utils():
    def __init__(self):
        self.org_id = 'odyssey-org'
        self.service_id = 'uclnlp-service'
        self.group_name = 'default_group'
        self.count = 0
        self.call_count = 0
        self.rpc_endpoints = rpc_endpoints
        self.snet_sdk = sdk.SnetSDK(config)
        self.start_time=time.time()
        self.proxy_port=7005
    
    def get_stance_classif(self, url):
        headline = exctract_headline(url)
        body = exctract_body(url)

        service_client = snet_sdk.create_service_client(
                self.org_id,
                self.service_id,
                pb2_grpc.UCLNLPStanceClassificationStub,
                group_name=self.group_name,
                concurrent_calls=1)
        
        req = pb2.InputData(headline=headline, body=body)
        result = service_client.service.stance_classify(req)

        return result



    

def exctract_headline(url):
    headline = 'Melania Trump cancels plans to attend Tuesday rally citing Covid recovery'
    return headline

def exctract_body(url):
    body = '''Melania Trump is canceling her first campaign appearance in
    months because she is not feeling well as she continues to recover from
    Covid-19.'''
    return body

