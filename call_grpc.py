import sys
import grpc

from extract import *

# import the generated classes
import uclnlp_service_pb2 as pb2
import uclnlp_service_pb2_grpc as pb2_grpc

uclnlp_endpoint = "demo.nunet.io:7007"
athene_endpoint = "demo.nunet.io:7008"
fakenews_endpoint = "demo.nunet.io:7009"

def call_grpc(url):    
    headline = extract_headline(url)
    body = extract_body(url)

    try:
        # Open a gRPC channel
		channel = grpc.insecure_channel("{}".format(uclnlp_endpoint))
		stub = pb2_grpc.UCLNLPStanceClassificationStub(channel)
		inp = pb2.InputData(headline=headline, body=body)
        
        # get result
        response = stub.stance_classify(inp)
		print(response)
    except Exception e:
        print(e)
        exit(1)
  
   return response

   
