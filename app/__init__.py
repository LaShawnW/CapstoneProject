from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_migrate import Migrate
import stripe 
from flask_googlemaps import GoogleMaps
from geopy.geocoders import GoogleV3
import csv
import sys
import logging



app = Flask(__name__)
socketio=SocketIO(app)

app.config['SECRET_KEY'] = "this is a super secure key"  # you should make this more random and unique
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:ilovemilk18@localhost/capstone"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # added just to suppress a warning


db = SQLAlchemy(app)
migrate = Migrate(app, db)

GoogleMaps(app)
geolocator = GoogleV3()


# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # necessary to tell Flask-Login what the default route is for the login page
login_manager.login_message_category = "info"  # customize the flash message category


public_key = 'pk_test_l5lotlN2Ys6OhMMYi6p7Wq7m00yAMKQtNO'
stripe.api_key = "	sk_test_W5gBcbCxQipyN94e9pPWm3Bu00Tfhvtrwk"
SECRET_KEY = 'Sup3r$3cretkey'



app.config.from_object(__name__)

from app import views
