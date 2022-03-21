from app import app
from flask import render_template

@app.route('/')
def FindHome():
    return render_template('index.html')

@app.route('/iphone')
def Findiphonecases():
  return render_template('iphone.html')


@app.route('/airpodcases')
def Findairpodcases():
  return render_template('airpod.html')









