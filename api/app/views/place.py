from app.models.place import Place
from app.models.city import City
from app.models.state import State
from flask_json import request
from app import app
from datetime import datetime

@app.route('/places', methods=['GET', 'POST'])
def places():
	if request.method == 'GET':
		list_places = Place.select()
		return json.dumps(list_places.to_hash())

	elif request.method == 'POST':
		data = request.data
		owner = data['owner_id']
		name = data['name']
		city = data['city']
		description = data['description']
		number_rooms = data['number_rooms']
		number_bathrooms = data['number_bathrooms']
		max_guest = data['max_guest']
		price_by_night = data['price_by_night']
		latitude = data['latitude']
		longitude = data['longitude']

		entry = Place.insert(owner=owner_id, name=name, city=city, description=description, number_rooms=number_rooms, number_bathrooms=number_bathrooms, max_guest=max_guest, price_by_night=price_by_night, latitude=latitude, longitude=longitude)
		entry.execute()