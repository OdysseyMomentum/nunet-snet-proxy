import subprocess
import json
import time

import rfakenews_service_pb2_grpc as pb2_grpc
import rfakenews_service_pb2 as pb2

from snet import sdk
from datetime import datetime

from config import config, rpc_endpoints


class utils():
    def __init__(self, org_id, service_id, group_name, rpc_endpoints, proxy_port):
        self.org_id = org_id
        self.service_id = service_id
        self.group_name = group_name
        self.count = 0
        self.call_count = 0
        self.rpc_endpoints = rpc_endpoints
        self.snet_sdk = sdk.SnetSDK(config)
        self.start_time=time.time()
        self.proxy_port=proxy_port
    


    def call_sdk(self, request, proc):
        self.call_count += 1
        service_client = self.snet_sdk.create_service_client(
                                    self.org_id,
                                    self.service_id,
                                    pb2_grpc.FNScoreStub,
                                    group_name=self.group_name,
                                    concurrent_calls=10
                        )
        
        try:
            response=getattr(service_client.service, proc)(request)
        except TypeError:
            if self.count == 0:
                self.account_deposit()
                response=getattr(service_client.service, proc)(request)
            else:
                time.sleep(300)
        except:
            response=getattr(service_client.service, proc)(request)

        return response
    
    def account_deposit(self):
        self.count = 1
        try:
            value=subprocess.check_output(["bash", "script.sh", "deposit"])
        except Exception as e:
            logging.exception("message", e)
        finally:
            self.count=0


