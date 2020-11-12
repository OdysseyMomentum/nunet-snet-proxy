import sys
import grpc

from extract import *

# import the generated classes
import uclnlp_service_pb2
import uclnlp_service_pb2_grpc

import athenefnc_pb2
import athenefnc_pb2_grpc

import fake_news_score_pb2
import fake_news_score_pb2_grpc

uclnlp_endpoint = "demo.nunet.io:7007"
athene_endpoint = "demo.nunet.io:7008"
fakenews_endpoint = "demo.nunet.io:7009"

service=""

def call_grpc(url):
    headline = extract_headline(url)
    body = extract_body(url)

    try:
        # Open a gRPC channel
        if service == "uclnlp":
            channel = grpc.insecure_channel("{}".format(uclnlp_endpoint))
            stub = uclnlp_service_pb2_grpc.UCLNLPStanceClassificationStub(channel)
            inp = uclnlp_service_pb2.InputData(headline=headline, body=body)
            # get result
            response = stub.stance_classify(inp)
            print(response)
        elif service == "athene":
            channel = grpc.insecure_channel("{}".format(athene_endpoint))
            stub = athenefnc_pb2_grpc.AtheneStanceClassificationStub(channel)
            inp = athenefnc_pb2.InputData(headline=headline, body=body)
            response = stub.stance_classify(inp)
            print(response)
        
        else :
            channel = grpc.insecure_channel("{}".format(fakenews_endpoint))
            stub = fake_news_score_pb2_grpc.FakeNewsScoreStub(channel)
            inp = fake_news_score_pb2.InputFNS(headline=headline, body=body)
            response = stub.fn_score_calc(inp)
            res = str(response).split('\n')
            res.pop(0)
            response = '\n'.join(map(str, res))
            print(response)


    except Exception as e:
        print(e)
        exit(1)

    return response
