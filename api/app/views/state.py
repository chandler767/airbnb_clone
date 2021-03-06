from app import app
from flask import request
from flask_json import json_response
from app.models.state import State
from flask import jsonify
from peewee import *
from return_styles import ListStyle

@app.route('/states', methods=['GET', 'POST'])
def states():
	if request.method == 'GET':
		query = State.select()

		return ListStyle.list(query, request), 200

	elif request.method == 'POST':
		try:
			if "name" not in request.form:
				return json_response(status_=400, msg="missing parameters", code=40000)

			insert = State(name=str(request.form["name"]))
			insert.save()
			return jsonify(insert.to_dict()), 201

		except IntegrityError:
			return json_response(status_=409,
								code=10001,
								msg="State already exists")

@app.route('/states/<state_id>', methods=['GET', 'DELETE'])
def states_id(state_id):
	if request.method == 'GET':
		try:
			state = State.get(State.id == state_id)
			return jsonify(state.to_dict()), 200

		except State.DoesNotExist:
			return json_response(status_=404, msg="not found")

	elif request.method == 'DELETE':
		try:
			state = State.get(State.id == state_id)
			state.delete_instance()
			state.save()
			return json_response(status_=200, msg="State succesfully deleted")

		except State.DoesNotExist:
			return json_response(status_=404, msg="state does not exist")