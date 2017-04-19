from flask import Flask
from flask_json import FlaskJSON
from flask_cors import CORS, cross_origin
import os

# initialize Flask application and FlaskJSON instance
app = Flask(__name__)
json = FlaskJSON(app)

if os.environ.get('AIRBNB_ENV') == 'development':
	CORS(app, resources=r"*", origins=["*"])
	app.config['CORS_HEADERS'] = 'Content-Type'

elif os.environ.get('AIRBNB_ENV') == 'production':
	CORS(app, resources=r"*", origins=["localhost", "54.183.231.35"])
	app.config['CORS_HEADERS'] = 'Content-Type'

from app.views import *