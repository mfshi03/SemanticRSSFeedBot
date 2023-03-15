

import json
import datetime
import requests
from functools import wraps
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup
from typing import List
from semantic_filter import listwise_ranking


app = Flask(__name__)
app.config['SECRET_KEY'] = 'chatgptsearch'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/test/', methods=['GET'])
def respond():
    name = request.args.get("msg", None)
    print(f"Received: {name}")

    response = {}

    if not name:
        response["ERROR"] = "No name found. Please send a name."

    elif str(name).isdigit():
        response["ERROR"] = "The name can't be numeric. Please send a string."
    else:
        response["MESSAGE"] = f"Your message: {name}"

    return jsonify(response)

@app.route('/preprocess',methods = ['POST', 'GET'])
def preprocess():
    query = request.get_json()['query']
    links = request.get_json()['results']
    titles = request.get_json()['titles']
    if links == None or len(links) == 0:
        return jsonify({'message': 'Links are missing!'}), 400
    if titles == None or len(links) == 0:
        return jsonify({'message': 'Titles are missing!'}), 400

    return jsonify({"success": "true"}) 

@app.route('/rank',methods = ['POST', 'GET'])
def rank():
    #query = "water"
    query = request.get_json()['query']
    if query == None or len(query) == 0:
        return jsonify({'message': 'Queries are missing!'}), 400

    response = {}
    ranked = listwise_ranking(query)
    response["Titles"] = ranked[0]
    response["Links"] = ranked[1]
    response["Scores"] = ranked[2]

    return jsonify(response)

     
    

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(threaded=True, port=5000)