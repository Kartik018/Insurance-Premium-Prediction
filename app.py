from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('Insurance.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        age=int(request.form['age'])
        bmi=float(request.form['bmi'])
        children=int(request.form['children'])
        sex=request.form['sex']
        if(sex=='male'):
            sex_male=1
        else:
            sex_male=0
        smoker=request.form['smoker']
        if(smoker=='Yes'):
            smoker_yes=1
        else:
            smoker_yes=0
        region=request.form['region']
        if(region=='northwest'):
            region_northwest=1
            region_southeast=0
            region_southwest=0
        elif(region=='southeast'):
            region_northwest=0
            region_southeast=1
            region_southwest=0
        elif(region=='southwest'):
            region_northwest=0
            region_southeast=0
            region_southwest=1
        else:
            region_northwest=0
            region_southeast=0
            region_southwest=0
        prediction=model.predict([[age,bmi,children,sex_male,smoker_yes,region_northwest,region_southeast,region_southwest]]) 
        output=round(prediction[0],2)
        if output<0:
            return render_template('Insurance.html',prediction_texts="Sorry can't predict")
        else:
            return render_template('Insurance.html',prediction_text="Insurance Premium expense is {}".format(output))
    else:
        return render_template('Isurance.html')
if __name__=="__main__":
    app.run(debug=True)

