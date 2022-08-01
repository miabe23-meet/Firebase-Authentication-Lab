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
  "databaseURL": "https://fir-cfa5b-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()

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
			user={
			"name": request.form['name'] ,
			"username": request.form['username'],
			"email": request.form['email'] ,
			"password": request.form['password'] , 
			"bio": request.form['bio']
			}
			db.child("users").child(login_session['user']['localId']).set(user)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
		return render_template("signup.html")
	return render_template("signup.html")




@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	if request.method == 'POST':
		title = request.form['title']
		text = request.form['text']
		try:
			tweet={
			"title": request.form['title'] ,
			"text": request.form['text'],
			"uid": login_session['user']['localId']
			}
			db.child("tweet").push(tweet)
			return redirect(url_for('all_tweets'))
		except:
			error = "Authentication failed"
		return render_template("add_tweet.html")
	return render_template("add_tweet.html")


	return render_template("add_tweet.html")


@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():
	tweets=db.child("tweet").get().val()
	return render_template("all_tweets.html", tweets=tweets)


if __name__ == '__main__':
	app.run(debug=True)