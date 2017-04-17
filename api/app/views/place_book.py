from app.models.place_book import PlaceBook
from app.models.place import Place
from app.models.user import User
from app import app
from datetime import datetime
import json
from flask import request, jsonify
from flask_json import json_response

@app.route('/places/<place_id>/books', methods=['GET', 'POST'])
def books(place_id):
	if request.method == 'GET':
		query = Place.select().where(Place.id == place_id)

		if not query.exists():
			return json_response(status_=404, msg="place does not exist")

		query = PlaceBook.select().where(PlaceBook.place == place_id)
		books = []

		for book in query:
			books.append(book.to_hash())

		return jsonify(books), 200

	elif request.method == 'POST':
		test = Place.select().where(Place.id == place_id)

		if test.wrapped_count() < 1:
			return json_response(status_=404, code=10002, msg="no place with such id")

		test = User.select().where(User.id == request.form["user"])

		if test.wrapped_count() < 1:
			return json_response(status_=404, msg="no user with given id")

		place_book = PlaceBook(place=place_id,
								user=request.form['user'],
								is_validated=request.form['is_validated'],
								date_start=datetime.strptime(request.form['date_start'], '%Y/%m/%d %H:%M:%S'),
								number_nights=request.form['number_nights'])
		place_book.save()
		return jsonify(place_book.to_hash()), 201

@app.route('/places/<place_id>/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def edit_books(place_id, book_id):
	if request.method == "GET":
		try:
			query = Place.select().where(Place.id == place_id)

			if not query.exists():
				return json_response(status_=404, msg="place does not exist")

			booking = PlaceBook.get(PlaceBook.id == book_id)
			return jsonify(booking.to_hash()), 200

		except PlaceBook.DoesNotExist:
			return json_response(code=404, status_=404, msg="Not found")


	elif request.method == "PUT":
		try:
			booking = PlaceBook.get(PlaceBook.id == book_id)

			for key in request.form:
				if key == "place":
					booking.place = request.form[key]

				elif key == "user":
					return json_response(status_=400, msg="Cant change user id")

				elif key == "is_validated":
					booking.is_validated = request.form[key]

				elif key == "date_start":
					booking.date_start = request.form[key]

				elif key == "number_nights":
					booking.number_nights = request.form[key]

			booking.save()
			return jsonify(booking.to_hash()), 200

		except PlaceBook.DoesNotExist:
			return json_response(code=404, status_=404, msg="Not found")

	elif request.method == "DELETE":
		try:
			booking = PlaceBook.get(PlaceBook.id == book_id)
			booking.delete_instance()
			booking.save()
			return json_response(status_=200, code=202, msg="Booking deleted")

		except PlaceBook.DoesNotExist:
			return json_response(code=404, status_=404, msg="Not found")