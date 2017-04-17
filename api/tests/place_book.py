from app import app
from app.models.base import database
from app.models.place_book import PlaceBook
from app.models.place import Place
from app.models.user import User
from app.models.city import City
from app.models.state import State

from datetime import datetime
import unittest
import json
import logging

from place import place_1, place_2
from user import user_1, user_2
from state import state_1
from city import city_1

booking_1 = dict(user=1, is_validated=False, date_start=datetime.now().strftime("%Y/%m/%d %H:%M:%S"), number_nights=1)
booking_2 = dict(is_validated=False, date_start=datetime.now().strftime("%Y/%m/%d %H:%M:%S"), number_nights=1)
booking_3 = dict(user=123, is_validated=False, date_start=datetime.now().strftime("%Y/%m/%d %H:%M:%S"), number_nights=1)
booking_4 = dict(user=1, is_validated=False, number_nights=1)

class PlaceBookUnitTest(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		logging.disable(logging.CRITICAL)

		database.connect()
		database.create_tables([PlaceBook, Place, User, State, City], safe=True)

		rv = self.app.post("/users", data=user_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post("/states", data=state_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post("/states/1/cities", data=city_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post("/places", data=place_1)
		self.assertEqual(rv.status_code, 201)

	def tearDown(self):
		database.drop_tables([PlaceBook, Place, User, State, City])
		database.close()

	def test_create(self):
		#Testing creation of a new booking
		rv = self.app.post("/places/1/books", data=booking_1)
		self.assertEqual(rv.status_code, 201)
		self.assertEqual(json.loads(rv.data)['id'], 1)

		#Testing creation of booking with invalid place
		rv = self.app.post("/places/123/books", data=booking_1)
		self.assertEqual(rv.status_code, 404)

		#Testing creation without user field
		rv = self.app.post('/places/1/books', data=booking_2)
		self.assertEqual(rv.status_code, 400)

		#Creation with non existent user
		rv = self.app.post('/places/1/books', data=booking_3)
		self.assertEqual(rv.status_code, 404)

		#Creation of booking with no datestart field
		rv = self.app.post('/places/1/books', data=booking_4)
		self.assertEqual(rv.status_code, 400)

	def test_list(self):
		#Test that there are no bookings
		rv = self.app.get("/places/1/books")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)), 0)

		#Creating new booking
		rv = self.app.post("/places/1/books", data=booking_1)
		self.assertEqual(rv.status_code, 201)

		#Testing that new booking is returned
		rv = self.app.get("/places/1/books")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)), 1)

	def test_get(self):
		#Creating booking
		rv = self.app.post("/places/1/books", data=booking_1)
		self.assertEqual(rv.status_code, 201)

		#Testing that booking is returned
		rv = self.app.get("/places/1/books/1")
		self.assertEqual(rv.status_code, 200)

		#Test I cant get a booking with invalid place
		rv = self.app.get("/places/123/books/1")
		self.assertEqual(rv.status_code, 404)

		#Test I cant get a booking with invalid booking id
		rv = self.app.get("/places/1/books/123")
		self.assertEqual(rv.status_code, 404)

	def test_delete(self):
		#Creating booking
		rv = self.app.post('/places/1/books', data=booking_1)
		self.assertEqual(rv.status_code, 201)

		#Testing that booking was created and returned
		rv = self.app.get('/places/1/books')
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)), 1)	

		#Deleting booking
		rv = self.app.delete('/places/1/books/1')
		self.assertEqual(rv.status_code, 200)

		#Checking place was deleted
		rv = self.app.get('/places/1/books')
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)), 0)

		#Testing to see if I can delete non-existent place
		rv = self.app.delete('/places/1/books/123')
		self.assertEqual(rv.status_code, 404)

	def test_update(self):
		#Creating booking
		rv = self.app.post('/places/1/books', data=booking_1)
		self.assertEqual(rv.status_code, 201)

		#Updating user
		rv = self.app.put("/places/1/books/1", data=dict(user=2))
		self.assertEqual(rv.status_code, 400)

		#Updating is_validated
		rv = self.app.put("/places/1/books/1", data=dict(is_validated=True))
		self.assertEqual(rv.status_code, 200)

		#Updating date start
		new_date_start = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		rv = self.app.put("/places/1/books/1", data=dict(date_start=new_date_start))
		self.assertEqual(rv.status_code, 200)

		#Updating number night
		rv = self.app.put("/places/1/books/1", data=dict(number_nights=2))
		self.assertEqual(rv.status_code, 200)

		#Adding second place
		rv = self.app.post("/places", data=place_2)
		self.assertEqual(rv.status_code, 201)

		#Updating place
		rv = self.app.put("/places/1/books/1", data=dict(place=2))
		self.assertEqual(rv.status_code, 200)

		#Checking that updated happened to the booking
		rv = self.app.get("/places/2/books/1")
		self.assertEqual(rv.status_code, 200)
		data = json.loads(rv.data)
		self.assertEqual(data["is_validated"], True)
		self.assertEqual(data["date_start"], new_date_start)
		self.assertEqual(data["number_nights"], 2)
		self.assertEqual(data["places"], 2)
