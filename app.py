# app.py - a flask api using flask_restful 
from flask import Flask, request, jsonify
from numpyencoder import NumpyEncoder

from utils import *

import json

app = Flask(__name__)

@app.route('/get_fake_news_score', methods=['POST', 'GET'])
def get_fake_news_score():
    if request.method=='POST':
        json_value=request.get_json()
        url=json_value['url']
        score=utils.calculate_fake_news_score(url)
        return str(score)
    else:
        url = request.args.get('url')
        score = utils.calculate_fake_news_score(url)
        return json.dumps(score, cls=NumpyEncoder)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=7000)