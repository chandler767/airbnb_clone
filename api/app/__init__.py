from flask import Flask
from flask_json import FlaskJSON

# initialize Flask application and FlaskJSON instance
app = Flask(__name__)
json = FlaskJSON(app)

from app.views import *