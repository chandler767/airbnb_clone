from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities
from app import app
import datetime
import json
from flask_json import request

@app.route('/amenities', methods=['GET', 'POST'])
def amenities():
	if request.method == 'GET':
		list_amenities = Amenity.select()
		return json_dumps(list_amenities.to_hash())

	elif request.method == 'POST':
		data = request.data
		name = data['name']

		entry = Amenity.insert(name=name)
		entry.execute()

@app.route('/amenities/<amenity_id>', methods=['GET', 'DELETE'])
def amenities_id(amenity_id):

	amenity = Amenity.select().where(id=amenity_id).get()
	if request.method == 'GET':
		return amenity.to_hash()

	elif request.method == 'DELETE':
		amenity.delete_instance()