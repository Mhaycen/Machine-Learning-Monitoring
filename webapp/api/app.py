from flask import render_template, request, jsonify
import flask
import numpy as np
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask_prometheus_metrics import register_metrics
import traceback
import pickle
import pandas as pd
import json


#App definition

app = flask.Flask(__name__,template_folder='templates')

#importing models
with open('model/models.pkl', 'rb') as f:
    classifier = pickle.load(f)

with open('model/model_columns.pkl', 'rb') as f:
    model_columns = pickle.load(f)



@app.route('/')
def welcome():
    return "Boston House Price Prediction"

@app.route('/predict', methods=['POST', 'GET'])
def predict():

    if flask.request.method == 'GET':
        return "Prediction Page"
    
    if flask.request.method == 'POST':
        try:
            json_ =request.json
            print(json_)
            query_ =pd.get_dummies(pd.DataFrame(eval((json_))))
            query = query_.reindex(columns = model_columns, fill_value = 0)
            prediction = list(classifier.predict(query))
            return jsonify({
                "prediction": prediction
            })
        except:
            return jsonify({
                "trace": traceback.format_exc()
            })
# provide app's version and deploy environment/config name to set a gauge metric
register_metrics(app, app_version="1.0",app_config="staging")
# plug metrics WSGI app to your main app with dispatcher
dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

if __name__ == "__main__":
    run_simple(hostname="localhost", port=5000, application=dispatcher)