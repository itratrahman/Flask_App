from flask import Flask, render_template, request, session, redirect, url_for
##importing the db object from models.py
from models import db, User, Place

##Importing the signup form class from the python file forms
from forms import SignupForm, LoginForm, AddressForm

##Creating a flask app instance
app = Flask(__name__)

##Configuring the database of the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tarti@localhost/learningflask'
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
@app.route("/signup", methods = ['GET', 'POST'])
def signup():

    if 'email' in session:

        return redirect(url_for('home'))

    ##Creating an object of signup form
    form = SignupForm()

    if request.method == 'POST':

        if form.validate() == False:

            return render_template('signup.html', form=form)

        else:

            ##Creating a new user
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            ##Creating a new session
            session['email'] = newuser.email
            return redirect(url_for('home'))


            return "Success!"

    elif request.method == 'GET':

        return render_template('signup.html', form=form)



@app.route("/login", methods=["GET", "POST"])
def login():

    if 'email' in session:

        return redirect(url_for('home'))

    form = LoginForm()

    if request.method == "POST":

        if form.validate() == False:

          return render_template("login.html", form=form)

        else:

            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()

            if user is not None and user.check_password(password):

                session['email'] = form.email.data

                return redirect(url_for('home'))

            else:

                return redirect(url_for('login'))

    elif request.method == 'GET':

        return render_template('login.html', form=form)



@app.route("/logout")
def logout():

    session.pop('email', None)

    return redirect(url_for('index'))


@app.route("/home", methods=["GET", "POST"])
def home():

    if 'email' not in session:

        return redirect(url_for('login'))

    form = AddressForm()

    places = []

    my_coordinates = (37.4221, -122.0844)

    if request.method == 'POST':

        if form.validate() == False:

            return render_template('home.html', form = form)

        else:

            # get the address
            address = form.address.data

            # query for places around it
            p = Place()
            my_coordinates = p.address_to_latlng(address)
            places = p.query(address)

            # return those results
            return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)

    elif request.method == 'GET':

        return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)


##The main method runs the app
if __name__ == "__main__":
  app.run(debug=True)