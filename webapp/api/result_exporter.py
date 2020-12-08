from prometheus_client import start_http_server, REGISTRY
from prometheus_client.core import  GaugeMetricFamily
import json
import requests
import time
import pandas as pd
import numpy as np
import csv
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
import flask

app = flask.Flask(__name__)

@app.route("/")
class JsonCollector(object) :


    def collect(self):

        model_result_metric = GaugeMetricFamily('model_result', 'Model Result', labels = {'prediction'})
        df = pd.read_csv(r"/mnt/c/Users/heyas/Documents/MLAPI/webapp/data/newHousing.csv", delimiter = ',', na_values="nan")
        for row in df.itertuples():
            features = [{'CRIM' : row.CRIM, 'ZN' : row.ZN, 'INDUS' : row.INDUS, 'CHAS' : row.CHAS, 'NOX' : row.NOX, 'RM' : row.RM, 'AGE' : row.AGE, 'DIS' : row.DIS, 'RAD' : row.RAD, 'TAX' : row.TAX, 'PTRATIO' : row.PTRATIO, 'B' : row.B, 'LSTAT' : row.LSTAT}]
            postrequest = json.dumps(features)
            response  = requests.post(url = 'http://127.0.0.1:5000/predict' , json = postrequest)            
            prediction = response.json()
            model_result_metric.add_metric('prediction_value', value = prediction['prediction'][0]) 
            
            yield model_result_metric

dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})
 
if __name__ == '__main__': 
        REGISTRY.register(JsonCollector())
        run_simple(hostname="localhost", port=8000, application=dispatcher)
