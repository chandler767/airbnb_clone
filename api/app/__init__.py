from flask import Flask
from flask_json import FlaskJSON
from views.amenity import *
from views.city import *
from views.index import *
from views.place import *
from views.place_book import *
from views.state import *
from views.user import *

# initialize Flask application and FlaskJSON instance
app = Flask(__name__)
json = FlaskJSON(app)