from flask import Flask, render_template
##importing the db object from models.py
from models import db

##Importing the signup form class from the python file forms
from forms import SignupForm

##Creating a flask app instance
app = Flask(__name__)

##Configuring the database of the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'
app.secret_key = "development-key"

db.init_app(app) ##initialize the flask app for using the database setup

##Creating a route for the homepage index.html
@app.route("/")
def index():
  return render_template("index.html")

##Creating a route for the about page
@app.route("/about")
def about():
    return render_template("about.html")

#Creating a route for the signup page
@app.route("/signup")
def signup():

    ##Creating an object of signup form
    form = SignupForm()

    return render_template('signup.html', form=form)


##The main method runs the app
if __name__ == "__main__":
  app.run(debug=True)