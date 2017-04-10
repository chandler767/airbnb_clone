from app.models.place_book import PlaceBook
from app.models.place import Place
from app.models.user import User
from app import app
from datetime import datetime
import json
from flask_json import request

@app.route('/places/<place_id>/books', methods=['GET', 'POST'])
def books(place_id):
	if request.method == 'GET':
		list_books = PlaceBook.select().where(PlaceBook.place == place_id)
		return json.dumps(list_books.to_hash())

	elif request.method == 'POST':
		data = request.data
		place = place_id
		user = data['user_id']
		is_validated = data['is_validated']
		date_start = data['date_start']
		number_nights = data['number_nights']

		entry = PlaceBook.insert(place=place, user=user, is_validated=is_validated,	date_start=date_start, number_nights=number_nights)
		entry.execute()

@app.route('/places/<place_id>/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def edit_books(place_id, book_id):
	pass