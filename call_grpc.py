import sys
import grpc
import os
from extract import *

# import the generated classes
import uclnlp_service_pb2
import uclnlp_service_pb2_grpc

import athenefnc_pb2
import athenefnc_pb2_grpc

import fake_news_score_pb2
import fake_news_score_pb2_grpc

uclnlp_grpc = os.getenv("UCLNLP_GRPC")
athene_grpc = os.getenv("ATHENE_GRPC")
fakenews_grpc = os.getenv("FAKENEWS_GRPC")
service=os.getenv("SERVICE")
print(service, flush=True)

def call_grpc(url):
    try:
        headline = extract_headline(url)
        body = extract_body(url)
    except Exception as e:
        print(e, flush=True)
        return "Invalid Url"

    try:
        # Open a gRPC channel
        if service == "uclnlp":
            channel = grpc.insecure_channel("{}".format(uclnlp_grpc))
            stub = uclnlp_service_pb2_grpc.UCLNLPStanceClassificationStub(channel)
            inp = uclnlp_service_pb2.InputData(headline=headline, body=body)
            # get result
            response = stub.stance_classify(inp)

        elif service == "athene":
            channel = grpc.insecure_channel("{}".format(athene_grpc))
            stub = athenefnc_pb2_grpc.AtheneStanceClassificationStub(channel)
            inp = athenefnc_pb2.InputData(headline=headline, body=body)
            response = stub.stance_classify(inp)
        
        elif service == "fakenews":
            channel = grpc.insecure_channel("{}".format(fakenews_grpc))
            stub = fake_news_score_pb2_grpc.FakeNewsScoreStub(channel)
            inp = fake_news_score_pb2.InputFNS(headline=headline, body=body)
            response = stub.fn_score_calc(inp)
            res = str(response).split('\n')
            res.pop(0)
            response = '\n'.join(map(str, res))


    except Exception as e:
        print(e)
        exit(1)
    print(response, flush=True)
    return response
