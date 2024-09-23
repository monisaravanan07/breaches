from flask import Flask, render_template, request, redirect, url_for,flash,session
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
warnings.filterwarnings('ignore')
from feature import FeatureExtraction
import time
import mysql.connector


conn=mysql.connector.connect(host="localhost",user="root",password="root",autocommit=True)
mycursor=conn.cursor(dictionary=True,buffered=True)
mycursor.execute("create database if not exists cyperwebsite")
mycursor.execute("use cyperwebsite")
mycursor.execute("create table if not exists cyper(id int primary key auto_increment,cname varchar(255),email varchar(30) unique,cpassword text)")

file = open("pickle/model.pkl","rb")
gbc = pickle.load(file)
file.close()


app = Flask(__name__)
app.secret_key = 'super secret key'
# UPLOAD_FOLDER = 'static'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def home():
    return render_template('index.html')




@app.route('/registration',methods =['GET', 'POST'])
def registration():
  if request.method == 'POST' and 'pass' in request.form and 'email' in request.form and 'hos' in request.form:
        name = request.form.get('pass')
        password=request.form.get('hos')
        mob = request.form.get('mob')
        email = request.form.get('email')
        mycursor.execute("SELECT * FROM cyper WHERE email = '"+ email +"' ")
        account = mycursor.fetchone()
        if account:
            flash('You are already registered, please log in')
        else:
            
            mycursor.execute("insert into cyper values(NULL,'"+ name +"','"+ email +"','"+ password +"')")
            # msg=flash('You have successfully registered !')
            return render_template("login.html")
        
  return render_template("register.html")

@app.route('/login',methods =['GET', 'POST'])
def login():
    if request.method == 'POST' and 'nm' in request.form and 'pass' in request.form:
        print('hello')
        email = request.form['nm']
        password = request.form['pass']
        
        mycursor.execute("SELECT * FROM cyper WHERE email = '"+ email +"' AND cpassword = '"+ password +"'")
        account = mycursor.fetchone()
        print(account)
        if account:
            session['loggedin'] = True
            session['email'] = account['email']
            msg = flash('Logged in successfully !')
                
            return render_template('predict.html')
        else:
            msg = flash('Incorrect username / password !')
            return render_template('login.html',msg=msg)
    return render_template('login.html')




import random

@app.route("/index", methods=["GET", "POST"])
def index():
    virus = {0: 'Spear Phishing', 1: 'Whaling', 2: 'Smishing', 3: 'Vishing'}
    if request.method == "POST":
        url = request.form["url"]
        print(url)
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1, 30)

        start_time = time.time()  # Record start time
        y_pred = gbc.predict(x)[0]
        print(y_pred)
        
        end_time = time.time()  # Record end time

        prediction_time = end_time - start_time  # Calculate time taken for prediction
        prediction_time_formatted = "{:.3f}".format(prediction_time)

        y_pro_phishing = gbc.predict_proba(x)[0, 0]
        y_pro_non_phishing = gbc.predict_proba(x)[0, 1]
       

        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing * 100)
       

        if y_pred == -1:  # Check if predicted vulnerability exists
            virus_name = random.choice(list(virus.values()))
            # virus_name= None
            # if url=="www.youtube.com":
            #     print("www.youtube.com1")
            #     virus_name= None
        else:
            virus_name = None

        return render_template('predict.html',
                               xx=round(y_pro_non_phishing, 2),
                               url=url,
                               y_pred=y_pred,
                               prediction_time=prediction_time_formatted,
                               virus_name=virus_name)

    return render_template("predict.html", xx=-1)



if __name__ == "__main__":
    app.run(debug=True)




# https://vpnoverview.com/privacy/anonymous-browsing/dark-web-websites-worth-visiting/