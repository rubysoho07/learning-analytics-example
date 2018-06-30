import json

from pymongo import MongoClient
from bson import ObjectId
from flask import Flask, render_template, request, abort

app = Flask(__name__)


# Database configuration
lrs = MongoClient('localhost')['LRS']['CaliperEvents']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/endpoint', methods=['POST'])
def endpoint():
    """ Endpoint to save learning record. """
    if request.method == 'POST':
        data = json.loads(request.data)
        result = lrs.insert(data)

        if type(result) is not ObjectId:
            abort(500)

        return str(result)
    else:
        abort(400)
