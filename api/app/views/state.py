from app import app
from flask import request
from flask_json import json_response
from app.models.base import database
from peewee import *

@app.route('/states', methods=['GET', 'POST'])
def states():
	if request.method == 'GET':
		list_states = State.select()
		return json.dumps(list_states.to_hash())

	elif request.method == 'POST':
		# get data from post request
		data = request.data
		name = data['name']
		
		# if name already exists in database, return error message
		name_check = State.get(State.name == name)
		if name_check:
			return json_response(code=10001, msg="State already exists")

		# if name_check is empty, create new state with post request info
		entry = State.insert(name=name)
		entry.execute()

		# return json of data added to State table
		state = State.select().where(name=name).get()
		return json.dumps(state.to_hash())

@app.route('/states/<state_id>', methods=['GET', 'DELETE'])
def states_id(state_id):
	state = State.select().where(id=state_id).get()

	if request.method == 'GET':
		return json.dumps(state.to_hash())

	elif request.method == 'DELETE':
		state.delete_instance()