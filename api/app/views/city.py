from app import app
from flask import request
from flask_json import json_response
from app.models.city import City
from flask import jsonify
from peewee import *
from return_styles import ListStyle

@app.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities(state_id):
	if request.method == 'GET':
		try:
			query = City.select().where(City.state == state_id)

			return ListStyle.list(query, request), 200

		except City.DoesNotExist:
			return json_response(status_=404, msg="not found")

	elif request.method == 'POST':
		if "name" not in request.form:
			return json_response(status_=400, msg="missing parameters", code=40000)

		city_test = City.select().where(City.name == str(request.form["name"]), City.state == state_id)

		if city_test.wrapped_count() > 0:
			return json_response(status_=409, code=10002, msg="city already exists in this state") 

		city = City(name=str(request.form["name"]), state=str(state_id))
		city.save()
		return jsonify(city.to_dict()), 201


@app.route('/states/<state_id>/cities/<city_id>', methods=["GET", "DELETE"])
def cities_states(state_id, city_id):
	if request.method == "GET":
		try:
			query = City.get(City.id == city_id)
			return jsonify(query.to_dict()), 200

		except City.DoesNotExist:
			return json_response(status_=404, msg="not found")


	elif request.method == "DELETE":
		try:
			city = City.get(City.id == city_id)

		except City.DoesNotExist:
			return json_response(status_=404, msg="Not found")

		city.delete_instance()
		city.save()
		return json_response(status_=200, msg="City deleted")