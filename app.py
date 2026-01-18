import os
import numpy as np
import pandas as pd

from flask import Flask, render_template, request
from customer_churn_prediction import logger
from customer_churn_prediction.pipeline.stage_06_prediction import PredictionPipeline


app = Flask(__name__) # initialize the flask app

@app.route("/", methods=['GET']) #route to display home page
def homePage():
    return render_template("index.html")

@app.route("/train", methods=['GET'])
def train():
    os.system("python main.py")
    return render_template("training_message.html")

@app.route("/predict",methods=['POST','GET'])
def index():
    logger.info(f"request: {[request,request.form]}")
    if request.method == 'POST':
        try:
            gender = request.form['gender']
            SeniorCitizen = int(request.form['SeniorCitizen'])
            Partner = request.form['Partner']
            Dependents = request.form['Dependents']
            PhoneService = request.form['PhoneService']
            MultipleLines = request.form['MultipleLines']
            OnlineSecurity = request.form['OnlineSecurity']
            OnlineBackup = request.form['OnlineBackup']
            DeviceProtection = request.form['DeviceProtection']
            TechSupport = request.form['TechSupport']
            StreamingTV = request.form['StreamingTV']
            StreamingMovies = request.form['StreamingMovies']
            tenure = int(request.form['tenure'])
            MonthlyCharges = float(request.form['MonthlyCharges'])
            Contract = request.form['Contract']
            InternetService = request.form['InternetService']
            PaymentMethod = request.form['PaymentMethod']
            PaperlessBilling = request.form['PaperlessBilling']

            data = {
                'gender':gender,
                'SeniorCitizen':SeniorCitizen,
                'Partner':Partner,
                'Dependents':Dependents,
                'PhoneService':PhoneService,
                'MultipleLines':MultipleLines,
                'OnlineSecurity':OnlineSecurity,
                'OnlineBackup':OnlineBackup,
                'DeviceProtection':DeviceProtection,
                'TechSupport':TechSupport,
                'StreamingTV':StreamingTV,
                'StreamingMovies':StreamingMovies,
                'tenure':tenure,
                'MonthlyCharges':MonthlyCharges,
                'Contract':Contract,
                'gendInternetServiceer':InternetService,
                'PaymentMethod':PaymentMethod,
                'PaperlessBilling':PaperlessBilling,
            }
            data = pd.DataFrame([data])
            logger.info(f"Data given to model: {[data,type(data)]}")
            obj = PredictionPipeline()
            status, prediction, msg = obj.predict(data)
            logger.info(f"Final prediction data: {[status, prediction, msg]}")
            if status:
                return render_template('result.html', prediction=str(prediction))
            else:
                return render_template(
                    'message.html', 
                    title="Something went wrong",
                    heading="Something went wrong",
                    message=msg,
                    category="danger",
                    icon="fas fa-times-circle",
                    primary_action={"label": "Home", "url": "/"}
                )
            
        except Exception as e:
            logger.info(f"Final prediction data exception : {e}")
            return render_template(
                    'message.html', 
                    title="Something went wrong",
                    heading="Final prediction failed",
                    message=e,
                    category="danger",
                    icon="fas fa-times-circle",
                    primary_action={"label": "Home", "url": "/"}
                )
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)