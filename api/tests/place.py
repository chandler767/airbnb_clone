from app import app
from app.models.base import database
from app.models.city import City
from app.models.place import Place
from app.models.place_book import PlaceBook
from app.models.user import User
from app.models.state import State

from state import state_1
from city import city_1
from user import user_1

import json
import unittest
import logging

place_1 = dict(owner_id=1, city=1, name="Place 1", description="Description of place 1", number_rooms=4, number_bathrooms=2, max_guest=8, price_by_night=200, latitude=41.31628, longitude=77.33703)
place_2 = dict(owner_id=1, city=1, name="Place 2", description="Description of place 2", number_rooms=4, number_bathrooms=2, max_guest=8, price_by_night=200, latitude=41.31628, longitude=77.33703)
place_3 = dict(city=1, name="Place 3", description="Description of place 3", number_rooms=4, number_bathrooms=2, max_guest=8, price_by_night=200, latitude=41.31628, longitude=77.33703)
place_4 = dict(owner_id=1, name="Place 4", description="Description of place 4", number_rooms=4, number_bathrooms=2, max_guest=8, price_by_night=200, latitude=41.31628, longitude=77.33703)
place_5 = dict(owner_id=1, city=1, description="Description of place 2", number_rooms=4, number_bathrooms=2, max_guest=8, price_by_night=200, latitude=41.31628, longitude=77.33703)

class PlaceUnitTest(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		logging.disable(logging.CRITICAL)

		database.connect()
		database.create_tables([City, State, Place, User, PlaceBook], safe=True)

		rv = self.app.post('/states', data=state_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/states/1/cities', data=city_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/users', data=user_1)
		self.assertEqual(rv.status_code, 201)

	def tearDown(self):
		database.drop_tables([City, State, Place, User, PlaceBook])
		database.close()

	def test_create(self):
		#Testing creation of new place
		rv = self.app.post('/places', data=place_1)
		self.assertEqual(rv.status_code, 201)
		self.assertEqual(json.loads(rv.data)['id'], 1)

		#Testing creation of place with pre-existing name
		rv = self.app.post('/places', data=place_1)
		self.assertEqual(rv.status_code, 409)

		#Testing creation of place with missing owner_id
		rv = self.app.post("/places", data=place_3)
		self.assertEqual(rv.status_code, 400)

		#Testing creation of place with missing city
		rv = self.app.post("/places", data=place_4)
		self.assertEqual(rv.status_code, 400)

		#Testing creation of place with missing name
		rv = self.app.post("/places", data=place_5)
		self.assertEqual(rv.status_code, 400)

	def test_list(self):
		#Test that there are no places
		rv = self.app.get("/places")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)["data"]), 0)

		#Creating a new place
		rv = self.app.post('/places', data=place_1)
		self.assertEqual(rv.status_code, 201)

		#Test that new place is returned
		rv = self.app.get("/places")
		self.assertEqual(len(json.loads(rv.data)["data"]), 1)

	def test_get(self):
		#Creating place
		rv = self.app.post('/places', data=place_1)
		self.assertEqual(rv.status_code, 201)

		#Testing that place is returned
		rv = self.app.get('/places/1')
		self.assertEqual(rv.status_code, 200)

		#Test that that I cant get test from non saved id
		rv = self.app.get("/places/123")
		self.assertEqual(rv.status_code, 404)

	def test_delete(self):
		#Creating place
		rv = self.app.post('/places', data=place_1)
		self.assertEqual(rv.status_code, 201)

		#Testing that place was created and returned
		rv = self.app.get('/places')
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)["data"]), 1)	

		#Deleting place
		rv = self.app.delete('/places/1')
		self.assertEqual(rv.status_code, 200)

		#Checking place was deleted
		rv = self.app.get('/places')
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)["data"]), 0)

		#Testing to see if I can delete non-existent place
		rv = self.app.delete('/places/123')
		self.assertEqual(rv.status_code, 404)

	def test_update(self):
		#Creating place
		rv = self.app.post('/places', data=place_1)
		self.assertEqual(rv.status_code, 201)

		#Updating name
		rv = self.app.put("/places/1", data=dict(name="New name"))
		self.assertEqual(rv.status_code, 200)

		#Updating description
		rv = self.app.put("/places/1", data=dict(description="New description"))
		self.assertEqual(rv.status_code, 200)

		#Updating number of rooms
		rv = self.app.put("/places/1", data=dict(number_rooms=3))
		self.assertEqual(rv.status_code, 200)

		#Updating number of bathrooms
		rv = self.app.put("/places/1", data=dict(number_bathrooms=1))
		self.assertEqual(rv.status_code, 200)

		#Updating max guests
		rv = self.app.put("/places/1", data=dict(max_guest=4))
		self.assertEqual(rv.status_code, 200)

		#Updating price by night 
		rv = self.app.put("/places/1", data=dict(price_by_night=150))
		self.assertEqual(rv.status_code, 200)

		#Updating lat
		rv = self.app.put("/places/1", data=dict(latitude=-3.6899))
		self.assertEqual(rv.status_code, 200)

		#Updating long
		rv = self.app.put("/places/1", data=dict(longitude=-98.2498))
		self.assertEqual(rv.status_code, 200)

		#Checking that updates happened
		rv = self.app.get('/places/1')
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(json.loads(rv.data)['name'], "New name")
		self.assertEqual(json.loads(rv.data)['description'], "New description")
		self.assertEqual(json.loads(rv.data)['number_rooms'], 3)
		self.assertEqual(json.loads(rv.data)['number_bathrooms'], 1)
		self.assertEqual(json.loads(rv.data)['max_guest'], 4)
		self.assertEqual(json.loads(rv.data)['price_by_night'], 150)
		self.assertEqual(json.loads(rv.data)['latitude'], -3.6899)
		self.assertEqual(json.loads(rv.data)['longitude'], -98.2498)

		#Testing update for invalid place
		rv = self.app.put("/places/123", data=dict(name="New name"))
		self.assertEqual(rv.status_code, 404)

		#Testing to see if I can update values that shouldnt be updated
		rv = self.app.put('/places/1', data=dict(owner_id=3))
		self.assertEqual(rv.status_code, 400)
		rv = self.app.put('/places/1', data=dict(city=3))
		self.assertEqual(rv.status_code, 400)

	def test_create_city_state(self):
		#Creating place via state/city endpoint
		rv = self.app.post('/states/1/cities/1/places', data=place_1)
		self.assertEqual(rv.status_code, 201)
		self.assertEqual(json.loads(rv.data)['id'], 1)

		#Testing creation of place with invalid state/city
		rv = self.app.post('/states/123/cities/1/places', data=place_1)
		self.assertEqual(rv.status_code, 404)

		rv = self.app.post('/states/1/cities/123/places', data=place_1)
		self.assertEqual(rv.status_code, 404)

	def test_list_city_state(self):
		#Testing that no place exists
		rv = self.app.get("/states/1/cities/1/places")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)["data"]), 0)

		#Creating place
		rv = self.app.post('/states/1/cities/1/places', data=place_1)
		self.assertEqual(rv.status_code, 201)

		#Testing if place was created and correctly returned
		rv = self.app.get("/states/1/cities/1/places")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)["data"]), 1)

		#Testing returning a place in invalid city
		rv = self.app.get("/states/1/cities/123/places")
		self.assertEqual(rv.status_code, 404)

		#Testing returning a place in invalid state
		rv = self.app.get("/states/123/cities/1/places")
		self.assertEqual(rv.status_code, 404)
