from app import app
from flask_json import json_response
from app.models.base import database
import datetime

# manages API route '/' and only allows GET request
@app.route('/', methods=["GET"])
# if request is successful, returns JSON with status and time
def index():
	utc = datetime.utcnow()
	now = datetime.datetime.now()
	return json_response(status='OK', utc_time=utc, time=now)

# opens database connection
def before_request():
	database.connect()

# closes database connection
def after_request():
	database.close()

# manages all routes that are not found
def not_found():
	return json_response(code='404', msg='not found')
