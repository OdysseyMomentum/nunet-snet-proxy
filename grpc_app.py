from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

from call_grpc import *

app = Flask(__name__)
CORS(app) # to enable CORS for the routes, unless from the front end response becomes Network Error

@app.route('/get_score', methods=['GET'])
def get_score():
   url = request.args.get('url')
   print("---g", flush=True)
   print(request, flush=True)
   result = call_grpc(url)
   print(result, flush=True)
   return str(result)
   
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("API_PORT"))
