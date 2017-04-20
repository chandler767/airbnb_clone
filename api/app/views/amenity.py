from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities
from app.models.place import Place
from app import app
import datetime
import json
from flask_json import request
from peewee import *
from flask import jsonify
from flask_json import json_response
from return_styles import ListStyle

@app.route('/amenities', methods=['GET', 'POST'])
def amenities():
	if request.method == 'GET':
		amenities = Amenity.select()
		return ListStyle.list(amenities, request), 200

	elif request.method == 'POST':
		try:
			if "name" not in request.form:
				return json_response(status_=400, msg="missing parameters", code=40000)
				
			test = Amenity.select().where(Amenity.name == request.form["name"])

			if test.wrapped_count() > 0:
				return json_response(status_=409, code=10002, msg="place already exists with this name")

			amenity = Amenity(name=request.form["name"])
			amenity.save()
			return jsonify(amenity.to_dict()), 201

		except IntegrityError:
			return json_response(status_=409,
								msg="Name already exists",
								code=10003)

@app.route('/amenities/<amenity_id>', methods=['GET', 'DELETE'])
def amenities_id(amenity_id):
	if request.method == 'GET':
		try:
			amenity = Amenity.select().where(Amenity.id == amenity_id)

		except Amenity.DoesNotExist:
			return json_response(status_=404, msg="Not found")

		return jsonify(amenity.to_dict()), 200

	elif request.method == 'DELETE':
		try:
			amenity = Amenity.get(Amenity.id == amenity_id)

		except Amenity.DoesNotExist:
			return json_response(status_=404, msg="Not found")

		amenity.delete_instance()
		amenity.save()
		return json_response(status_=200, msg="Amenity deleted")


@app.route("/places/<place_id>/amenities", methods=["GET"])
def amenities_place(place_id):
	if request.method == "GET":
		try:
			query = Amenity.select().join(PlaceAmenities).where(PlaceAmenities.place == place_id)
			return ListStyle.list(query, request), 200

		except:
			return json_response(status_=404, msg="Not found")

@app.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST", "DELETE"])
def place_amenity_id(place_id, amenity_id):
	query = Place.select().where(Place.id == place_id)

	if query.wrapped_count() < 1:
		return json_response(status_=404, msg="that place does not exist")

	query = Amenity.select().where(Amenity.id == amenity_id)

	if query.wrapped_count() < 1:
		return json_response(status_=404, msg="that amenity does not exist")

	query = PlaceAmenities.select().where(PlaceAmenities.amenity == amenity_id, PlaceAmenities.place == place_id)

	if query.wrapped_count() > 0:
		return json_response(status_=404, msg="amenity already set for given place")

	if request.method == "POST":
		insert = PlaceAmenities(place=place_id, amenity=amenity_id)
		insert.save()
		return jsonify(insert.to_dict()), 201

	elif request.method == "DELETE":
		amenity = PlaceAmenities.get(PlaceAmenities.amenity == amenity_id, PlaceAmenities.place == place_id)
		amenity.delete_instance()
		amenity.save()
		return json_response(status_=200, msg="amentiy delete for given place")