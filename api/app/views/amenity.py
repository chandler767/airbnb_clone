from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities
from app import app
import datetime
import json
from flask_json import request
from peewee import *
from flask import jsonify
from flask_json import json_response

@app.route('/amenities', methods=['GET', 'POST'])
def amenities():
	if request.method == 'GET':
		amenities = Amenity.select()
		data = []

		for a in amenities:
			data.append(a.to_hash())

		return jsonify(data), 200

	elif request.method == 'POST':
		try:
			if "name" not in request.form:
				return json_response(status_=400, msg="missing name field")
				
			test = Amenity.select().where(Amenity.name == request.form["name"])

			if test.wrapped_count() > 0:
				return json_response(status_=409, code=10002, msg="place already exists with this name")

			amenity = Amenity(name=request.form["name"])
			amenity.save()
			return jsonify(amenity.to_hash()), 201

		except IntegrityError:
			return json_response(status_=409,
								msg="Name already exists",
								code=10003)

@app.route('/amenities/<amenity_id>', methods=['GET', 'DELETE'])
def amenities_id(amenity_id):
	if request.method == 'GET':
		try:
			amenity = Amenity.get(Amenity.id == amenity_id)

		except Amenity.DoesNotExist:
			return json_response(status_=404, msg="Not found")

		return jsonify(amenity.to_hash()), 200

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
			return jsonify(query.to_hash()), 200

		except:
			return json_response(status_=404, msg="Not found")