from app.models.place_book import PlaceBook
from app.models.place import Place
from app.models.user import User
from app import app
from datetime import datetime, timedelta
import json
from flask import request, jsonify
from flask_json import json_response
from return_styles import ListStyle

@app.route('/places/<place_id>/books', methods=['GET', 'POST'])
def books(place_id):
	if request.method == 'GET':
		query = Place.select().where(Place.id == place_id)

		if not query.exists():
			return json_response(status_=404, msg="place does not exist")

		query = PlaceBook.select().where(PlaceBook.place == place_id)
		return ListStyle.list(query, request), 200

	elif request.method == 'POST':
		if "name" not in request.form or "date_start" not in request.form:
			return json_response(status_=400, code=40000, msg="missing parameters")

		test = Place.select().where(Place.id == place_id)

		if test.wrapped_count() < 1:
			return json_response(status_=404, code=10002, msg="no place with such id")

		test = User.select().where(User.id == request.form["user"])

		if test.wrapped_count() < 1:
			return json_response(status_=404, msg="no user with given id")

		try:
			start = datetime.strptime(request.form['date_start'], '%Y/%m/%d %H:%M:%S')

		except ValueError:
			return json_response(status_=400, msg="incorrect date format")

		end = start + timedelta(days=int(request.form['number_nights']))
		bookings = PlaceBook.select().where(PlaceBook.place == place_id)

		for booking in bookings:
			start_b = booking.date_start
			end_b = start_date + timedelta(days=booking.number_nights)

			if start >= start_b and start < end_b:
				return json_response(status=410, msg="Place unavailable at this date", code=110000)

			elif start_b >= start and start_b < end:
				return json_response(status=410, msg="Place unavailable at this date", code=110000)

			elif end > start_b  and end <= end_b:
				return json_response(status=410, msg="Place unavailable at this date", code=110000)

		place_book = PlaceBook(place=place_id,
								user=request.form['user'],
								date_start=datetime.strptime(request.form['date_start'], '%Y/%m/%d %H:%M:%S'))

		if "is_validated" in request.form:
			place_book.is_validated = request.form["is_validated"]

		elif "number_nights" in request.form:
			place_book.number_nights = request.form["number_nights"]

		place_book.save()
		return jsonify(place_book.to_dict()), 201

@app.route('/places/<place_id>/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def edit_books(place_id, book_id):
	if request.method == "GET":
		try:
			query = Place.select().where(Place.id == place_id)

			if not query.exists():
				return json_response(status_=404, msg="place does not exist")

			booking = PlaceBook.get(PlaceBook.id == book_id)
			return jsonify(booking.to_dict()), 200

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
			return jsonify(booking.to_dict()), 200

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