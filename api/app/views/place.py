from app.models.place import Place
from app.models.city import City
from app.models.state import State
from flask_json import json_response
from app import app
from datetime import datetime
from peewee import *
from flask import jsonify, request

@app.route('/places', methods=['GET', 'POST'])
def places():
	if request.method == 'GET':
		list_places = Place.select()
		places = []
		for place in list_places:
			places.append(place.to_hash())

		return jsonify(places), 200

	elif request.method == 'POST':
		test = Place.select().where(Place.name == request.form["name"])

		if test.wrapped_count() > 0:
			return json_response(status_=409, code=10002, msg="place already exists with this name")

		try:
			entry = Place(owner=request.form["owner_id"], name=request.form["name"], city=request.form["city"], description=request.form["description"],
						number_rooms=int(request.form["number_rooms"]), number_bathrooms=int(request.form["number_bathrooms"]),
						max_guest=int(request.form["max_guest"]), price_by_night=int(request.form["price_by_night"]),
						latitude=float(request.form["latitude"]), longitude=float(request.form["longitude"]))
			entry.save()
			return jsonify(entry.to_hash()), 201

		except IntegrityError:
			return json_response(status_=400, msg="you are missing a field in your post request")


@app.route("/places/<place_id>", methods=["GET", "PUT", "DELETE"])
def place_id(place_id):
	if request.method == "GET":
		try:
			place = Place.get(Place.id == place_id)
			return jsonify(place.to_hash()), 200

		except Place.DoesNotExist:
			return json_response(status_=404, code=404, msg="Not found")

	elif request.method == "PUT":
		try:
			place = Place.get(Place.id == place_id)

		except Place.DoesNotExist:
			return json_response(status_=404, code=404, msg="Not found")

		for key in request.form:
			if key == "name":
				place.name = request.form[key]

			elif key == "description":
				place.description = request.form[key]

			elif key == "number_rooms":
				place.number_rooms = request.form[key]

			elif key == "number_bathrooms":
				place.number_bathrooms = request.form[key]

			elif key == "max_guest":
				place.max_guest = request.form[key]

			elif key == "price_by_night":
				place.price_by_night = request.form[key]

			elif key == "latitude":
				place.latitude = request.form[key]

			elif key == "longitude":
				place.longitude = request.form[key]

			elif key == "owner_id":
				return json_response(status_=400, msg="Cant update owner id")

			elif key == "city":
				return json_response(status_=400, msg="Cant update city id")

		place.save()

		return jsonify(place.to_hash()), 200

	elif request.method == "DELETE":
		try:
			place = Place.get(Place.id == place_id)

		except Place.DoesNotExist:
			return json_response(code=404, status_=404, msg="Not found")

		place.delete_instance()
		place.save()
		return json_response(status_=200, msg="Place deleted")


@app.route("/states/<state_id>/cities/<city_id>/places", methods=["GET", "POST"])
def state_city_place(state_id, city_id):
	if request.method == "GET":
		try:
			state_test = State.select().where(State.id == state_id)

			if state_test.wrapped_count() < 1:
				return json_response(status_=404, code=10002, msg="state not found") 

			city_test = City.select().where(City.id == city_id)

			if city_test.wrapped_count() < 1:
				return json_response(status_=404, code=10002, msg="state not found") 

			places = []
			query = Place.select().where(Place.city == city_id)
			for place in query:
				places.append(place.to_hash())

			return jsonify(places), 200

		except Place.DoesNotExist:
			return json_response(status_=404, code=404, msg="not found")

	elif request.method == "POST":
		try:
			city = City.get(City.id == city_id, City.state_id == state_id)

		except City.DoesNotExist:
			return json_response(status_=404, msg="City does not exist")

		try:
			place = Place(owner=request.form['owner_id'],
						city=city_id,
						name=request.form['name'],
						description=request.form['description'],
						number_rooms=request.form['number_rooms'],
						number_bathrooms=request.form['number_bathrooms'],
						max_guest=request.form['max_guest'],
						price_by_night=request.form['price_by_night'],
						latitude=request.form['latitude'],
						longitude=request.form['longitude'] )

			place.save()

		except IntegrityError:
			return json_response(status_=409, msg="Name already exists")

        return jsonify(place.to_hash()), 201