from flask_json import json_response
from app.models.base import database
from app import app
from datetime import datetime

# manages API route '/' and only allows GET request
@app.route('/', methods=["GET"])
# if request is successful, returns JSON with status and time
def index():
	utc = str(datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S'))
	now = str(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
	return json_response(status='OK', utc_time=utc, time=now)

# opens database connection
def before_request():
	database.connect()

# closes database connection
def after_request():
	database.close()

# manages all routes that are not found
@app.errorhandler(404)
def not_found(e):
	return json_response(status=404, code=404, msg='not found')
