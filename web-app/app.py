from flask import Flask, url_for, render_template, redirect
from forms import PredictForm
from flask import request, sessions
import requests
from flask import json
from flask import jsonify
from flask import Request
from flask import Response
import urllib3
import json
# from flask_wtf import FlaskForm

app = Flask(__name__, instance_relative_config=False)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'development key' #you will need a secret key

if __name__ == "__main__":
  #uncomment following line for localhost run
  #app.run(debug=True, host='0.0.0.0')
  app.run(host='0.0.0.0', port=8080)

@app.route('/', methods=('GET', 'POST'))

def startApp():
    form = PredictForm()
    return render_template('index.html', form=form)

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()
    if form.submit():

        # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer '
                 + " Bearer eyJraWQiOiIyMDIxMDcxOTE4MzciLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02NzIwMDBLQjcwIiwiaWQiOiJJQk1pZC02NzIwMDBLQjcwIiwicmVhbG1pZCI6IklCTWlkIiwic2Vzc2lvbl9pZCI6IkMtNGIyZjc1ODktMWM4Yy00ZTEwLWIyNzctMDhiMjY2YWM1M2IwIiwianRpIjoiMGMyYWQ2YjQtNmZhMC00MDI2LTk4MGEtYjVmMTYxNzc3YThiIiwiaWRlbnRpZmllciI6IjY3MjAwMEtCNzAiLCJnaXZlbl9uYW1lIjoiU0ciLCJmYW1pbHlfbmFtZSI6IlRocmVlIiwibmFtZSI6IlNHIFRocmVlIiwiZW1haWwiOiJzZ3VuaXRlZGFpcDEwMDNAZ21haWwuY29tIiwic3ViIjoic2d1bml0ZWRhaXAxMDAzQGdtYWlsLmNvbSIsImF1dGhuIjp7InN1YiI6InNndW5pdGVkYWlwMTAwM0BnbWFpbC5jb20iLCJpYW1faWQiOiJJQk1pZC02NzIwMDBLQjcwIiwibmFtZSI6IlNHIFRocmVlIiwiZ2l2ZW5fbmFtZSI6IlNHIiwiZmFtaWx5X25hbWUiOiJUaHJlZSIsImVtYWlsIjoic2d1bml0ZWRhaXAxMDAzQGdtYWlsLmNvbSJ9LCJhY2NvdW50Ijp7ImJvdW5kYXJ5IjoiZ2xvYmFsIiwidmFsaWQiOnRydWUsImJzcyI6IjcxNDI0NWRlYTUyZTQzOTE4NmVjMjA3YmIyYzFmNjgzIn0sImlhdCI6MTYyODc1ODkzMywiZXhwIjoxNjI4NzYwMTMzLCJpc3MiOiJodHRwczovL2lhbS5jbG91ZC5pYm0uY29tL2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InBhc3N3b3JkIiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiYngiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.3BKAbKRGItvrcXkuV2-cw8iArbX4uQ2oOyT62-PdL87LLBdRYYYka1-V4_Or9dOxJj3toPA4XnOTP0SopZ1UnCkr5MrVb-4cc4fhB0P19V6N68cRu2Rdqu0Ff90u_2IECTCrWMgSut4kcbUSWOXSwhKk9FDUq9dhXCDzUTvUmv6C1TcMuHookOCE7iAWQZTETlaBnXEF7aW34bfiGeykpGa_jYgXsBBHiPpNOVzXpFHdR0kBT3mM45B3h8-bnblDbtlB8fpXaFt7zetv93yrGl9XcgPJlF7rCFTl-4aPHJ_LozY1ExZOKOAiDYq5qqEMPheTed7T-0VY_ErAM2m8RQ"}

        if(form.bmi.data == None): 
          python_object = []
        else:
          python_object = [form.age.data, form.sex.data, float(form.bmi.data),
            form.children.data, form.smoker.data, form.region.data]
        #Transform python objects to  Json

        userInput = []
        userInput.append(python_object)

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"fields": ["age", "sex", "bmi",
          "children", "smoker", "region"], "values": userInput }]}

        response_scoring = requests.post("https://us-south.ml.cloud.ibm.com/ml/v4/deployments/7f300534-3cb3-49be-988d-0216cfa860c9/predictions?version=2021-08-13", json=payload_scoring, headers=header)

        output = json.loads(response_scoring.text)
        print(output)
        for key in output:
          ab = output[key]
        

        for key in ab[0]:
          bc = ab[0][key]
        
        roundedCharge = round(bc[0][0],2)

  
        form.abc = roundedCharge # this returns the response back to the front page
        return render_template('index.html', form=form)
