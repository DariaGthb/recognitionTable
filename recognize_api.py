import datetime
import sys

from flask import Flask, request
from flask_restful import Api, Resource
import correctImage
import base64
import cv2
import os
import tempfile
import json
from sys import platform
import numpy as np


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['RESTFUL_JSON'] = {'ensure_ascii': False}
api = Api(app)


class Quote(Resource):
    def get(self, id=0):
        return f"must use POST method", 200

    def post(self, id=0):

        try:
            file = request.get_json()
            if type(file) != dict:
                return f"POST data must be JSON: object with fields 'file','extension','coordinates'", 201
        except:
            return f"POST data must be JSON: object with fields 'file','extension', 'coordinates'", 201
        result = []

        try:
            data = base64.b64decode(file["file"])
        except:
            result.append({'id_file': file["id_file"], 'error': r"file must be in base64"})

        fhandle, fname = tempfile.mkstemp(suffix='.' + str(file["extension"]), dir=tempfile.gettempdir())

        try:
            with open(fname, 'wb') as f:
                f.write(data)
            os.close(fhandle)
        except:
            os.close(fhandle)
            os.remove(fname)
            result.append({'error': r"error save file"})

        try:
            FileResult = []
            print('list ' + str(1) + ' ' + fname + ' ' + str(datetime.datetime.now()))
            image = cv2.imread(fname)
            coordinates = np.array(file["coordinates"])
            cropped_image = correctImage.cropImg(image, coordinates)


            result.append({'result': "success"})
        except:
            result.append({'error': str(sys.exc_info()[1])})
        os.remove(fname)

        # Теперь нужно распределить результат
        return json.dumps(result, ensure_ascii=False), 202

    def put(self, id=0):
        return f"must use POST method", 201

    def delete(self, id=0):
        return f"must use POST method", 200


@app.route('/')
def hello():
    return platform


api.add_resource(Quote, "/recognize", "/recognize/", "/recognize/<int:id>")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=False)
    #app.run(debug=True)
