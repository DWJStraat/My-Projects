import flask
from flask_restful import request, Api, Resource, reqparse
import pandas as pd
import ast
import json


app = flask.Flask(__name__)
api = Api(app)

class remote_API(Resource):
    def __init__(self, json_file):
        self.json_file = json_file
        self.json = pd.read_json(self.json_file)
    def post(self):
        data = request.get_json()
        print(data)
        return {'data': 'Hello World'}, 200
    def get(self):
        return {'data': 'Hello World'}, 200



api.add_resource(remote_API, '/remote_api')



if __name__ == '__main__':
    app.run('test.json', debug=True)