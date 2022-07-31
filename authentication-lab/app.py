from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


config= {
  "apiKey": "AIzaSyA2L6-df-klrNcmF4DELH7pgO74OLN5MU4",
  "authDomain": "fir-cfa5b.firebaseapp.com",
  "projectId": "fir-cfa5b",
  "storageBucket": "fir-cfa5b.appspot.com",
  "messagingSenderId": "949101888347",
  "appId": "1:949101888347:web:2cfb886b3e4e9e5250907e",
  "measurementId": "G-Z6G20GVL9W",
  "databaseURL": ""
}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()

@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
       except:
           error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)