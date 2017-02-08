from flask.ext.sqlalchemy import SQLAlchemy ##Importing SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

##Creating an object of SQLAlchemy
db = SQLAlchemy()


##Creating the database model
class User(db.Model):


    ##Creating a table by the name of users
    __tablename__ = 'users'

    ##A column for user id which act as the primary key
    uid = db.Column(db.Integer, primary_key = True)

    ##A column for the firstname of type string
    firstname = db.Column(db.String(100))

    ##A column for the lastname of type string
    lastname = db.Column(db.String(100))

    ##A column for email of type string and is unique
    email = db.Column(db.String(120), unique=True)

    ##A column for password of type string
    pwdhash = db.Column(db.String(54))

    ##Class constructor
    def __init__(self, firstname, lastname, email, password):

        ##Class fields initialized by the constructor
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password) ##set_password function is invoked
                                    ##to generate a password hash for security


    def set_password(self, password):

        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):

        return check_password_hash(self.pwdhash, password)





