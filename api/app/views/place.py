from app.models.place import Place
from app.models.city import City
from app.models.state import State
from app.models.place_book import PlaceBook
from flask_json import json_response
from app import app
from datetime import datetime, timedelta
from peewee import *
from flask import jsonify, request
from return_styles import ListStyle

@app.route('/places', methods=['GET', 'POST'])
def places():
	if request.method == 'GET':
		list_places = Place.select()
		
		return ListStyle.list(list_places, request), 200

	elif request.method == 'POST':
		if "name" not in request.form or "owner_id" not in request.form or "city" not in request.form:
			return json_response(status_=400, code=40000, msg="missing parameters")

		test = Place.select().where(Place.name == request.form["name"])

		if test.wrapped_count() > 0:
			return json_response(status_=409, code=10002, msg="place already exists with this name")

		try:
			entry = Place(owner=request.form["owner_id"], name=request.form["name"], city=request.form["city"])

			if request.form['description']:
				entry.description = str(request.form['description'])

			if request.form['number_rooms']:
				entry.number_rooms = int(request.form['number_rooms'])

			if request.form['number_bathrooms']:
				entry.number_bathrooms = int(request.form['number_bathrooms'])

			if request.form['max_guest']:
				entry.max_guest = int(request.form['max_guest'])

			if request.form['price_by_night']:
				entry.price_by_night = int(request.form['price_by_night'])

			if request.form['latitude']:
				entry.latitude = float(request.form['latitude'])

			if request.form['longitude']:
				entry.longitude = float(request.form['longitude'])

			entry.save()
			return jsonify(entry.to_dict()), 201

		except IntegrityError:
			return json_response(status_=400, msg="you are missing a field in your post request")


@app.route("/places/<place_id>", methods=["GET", "PUT", "DELETE"])
def place_id(place_id):
	if request.method == "GET":
		try:
			place = Place.get(Place.id == place_id)
			return jsonify(place.to_dict()), 200

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

		return jsonify(place.to_dict()), 200

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

			query = Place.select().where(Place.city == city_id)

			return ListStyle.list(query, request), 200

		except Place.DoesNotExist:
			return json_response(status_=404, code=404, msg="not found")

	elif request.method == "POST":
		if "name" not in request.form or "owner_id" not in request.form:
			return json_response(status_=400, code=40000, msg="missing parameters")

		try:
			city = City.get(City.id == city_id, City.state_id == state_id)

		except City.DoesNotExist:
			return json_response(status_=404, msg="City does not exist")

		try:
			place = Place(owner=request.form['owner_id'],
						city=city_id,
						name=request.form['name'])

			if request.form['description']:
				place.description = str(request.form['description'])

			if request.form['number_rooms']:
				place.number_rooms = int(request.form['number_rooms'])

			if request.form['number_bathrooms']:
				place.number_bathrooms = int(request.form['number_bathrooms'])

			if request.form['max_guest']:
				place.max_guest = int(request.form['max_guest'])

			if request.form['price_by_night']:
				place.price_by_night = int(request.form['price_by_night'])

			if request.form['latitude']:
				place.latitude = float(request.form['latitude'])

			if request.form['longitude']:
				place.longitude = float(request.form['longitude'])

			place.save()

		except IntegrityError:
			return json_response(status_=409, msg="Name already exists")

        return jsonify(place.to_dict()), 201

@app.route("/states/<state_id>/places", methods=["GET"])
def state_places(state_id):
	state = State.select().where(State.id == state_id)

	if state.wrapped_count() < 1:
		return json_response(status_=404, code=10002, msg="state not found")

	query = Place.select().join(City).join(State).where(State.id == state_id)

	return ListStyle.list(query, request)

@app.route("/places/<place_id>/available", methods=["POST"])
def place_available(place_id):
	if "year" not in request.form or "month" not in request.form or "day" not in request.form:
		return json_response(status_=400, code=40000, msg="missing parameters")

	place = Place.select().where(Place.id == place_id)

	if place.wrapped_count() < 1:
		return json_response(status_=404, msg="place does not exist")

	request_date = datetime.strptime(str(request.form["day"]) + str(request.form["month"]) + str(request.form["year"]), "%d%m%Y")

	bookings = PlaceBook.select().where(PlaceBook.place == place_id)

	for booking in bookings:
		start_date = datetime.strptime(booking.date_start.strftime("%d%m%Y"), "%d%m%Y")
		end_date = start_date + timedelta(days=booking.number_nights)
		if end_date >= request_date >= start_date:
			return jsonify({'available': False}), 200 

	return jsonify({'available': True}), 200
