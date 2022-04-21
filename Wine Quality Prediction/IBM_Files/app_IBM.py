from flask import Flask, render_template, request # Flask is a application
# used to run/serve our application
# request is used to access the file which is uploaded by the user in out application
# render_template is used for rendering the html pages
import pickle # pickle is used for serializing and de-serializing Python object structures

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "vJFrz7R7INcTcwg19O_7jCvKTJQSO3fz1p3oR6HobCEl"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app=Flask(__name__) # our flask app

@app.route('/') # rendering the html template
def home():
    return render_template('h.html')
@app.route('/predict') # rendering the html template
def index() :
    return render_template("index.html")

@app.route('/data_predict', methods=['GET','POST']) # route for our prediction
def predict():
    
    # loading model which we saved
    model = pickle.load(open('wineQuality_new.pkl', 'rb'))
 
    data = [[x for x in request.form.values()]]    
    
    pred= model.predict(data)[0]
    print(pred)
    if pred==0:
        prediction="Bad"
    else:
        prediction="Good"
    #payload_scoring = {"input_data": [{"fields": ['Bad','Good'], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}

    #response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/73c68f6c-2a68-4065-8a6e-3041a1326060/predictions?version=2022-03-07', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    
    return render_template('pred.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)