from flask import Flask, render_template, request, Response, jsonify
from werkzeug.datastructures import ImmutableMultiDict
from predictor import predictor
import logging
import pandas as pd
import joblib
import json


new_data = {
    'INCOME': 125301.0,
    'OCCUPATION': 'z_Blue Collar',
    'TRAVTIME' : 46.0,
    'CAR_USE': 'Commercial',
    'BLUEBOOK': 17430.0,
    'CAR_TYPE': 'Sports Car',
    'OLDCLAIM': 0,
    'CLM_FREQ': 0,
    'REVOKED': 'No',
    'MVR_PTS': 0,
    'CLM_AMT': 2946.0,
    'CAR_AGE': 7
}

logging.basicConfig(level=logging.ERROR, filemode='w', filename='error_log.log', format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)


def index_page(prediction):
     return render_template('result.html', prediction=prediction)

def error_page(error):
     return render_template('error.html', error=error)

@app.route("/result")
def result():
        
        data = {}
        immut_dict = request.args

        for key, value in immut_dict.items():
            if isinstance(value, list):
                data[key] = value[0] if len(value) > 0 else None
            else:
                data[key] = value
        
            
        output = predictor(data)
        if output == 1:
            prediction = 'Insurance can be claimed'
            return index_page(prediction=prediction)
        elif output == 0:
            prediction = "Insurance can't be claimed"
            return index_page(prediction=prediction)
        elif output == 2:
            error = "Service not Available due to internal problem"
            return error_page(error=error)
        