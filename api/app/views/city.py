from app import app
from flask import request
from flask_json import json_response
from app.models.base import database
from peewee import *

@app.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities(state_id):
	if request.method == 'GET':
		list_cities = (City.select(State, City).join(State).where(State.id == state_id))
		return json.dumps(list_cities.to_hash())

	elif request.method == 'POST':
		# get data from post request
		data = request.data
		name = data['name']
		state = state_id

		# if name already exists in selected state database, return error message
		name_check = City.select()(User.email == email)
		if name_check:
			return json_response(code=10000, msg="Email already exists")

		# if email_check is empty, create new user with post request info
		entry = User.insert(first_name=first_name, last_name=last_name, email=email, password=User.set_password(password))
		entry.execute()

		# return json of data added to User table
		user = User.select().where(first_name=first_name, last_name=last_name, email=email).get()
		return json.dumps(user.to_hash())