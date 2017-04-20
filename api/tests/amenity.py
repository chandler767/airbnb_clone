from app import app
from app.models.base import database
from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities
from app.models.place import Place
from app.models.state import State
from app.models.user import User
from app.models.city import City

import json
import unittest
import logging

from state import state_1
from city import city_1
from user import user_1
from place import place_1

amenity_1 = dict(name="Amenity 1")

class AmenityUnitTest(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		logging.disable(logging.CRITICAL)

		database.connect()
		database.create_tables([Amenity, PlaceAmenities, Place, State, User, City], safe=True)

	def tearDown(self):
		database.drop_tables([Amenity, PlaceAmenities, Place, State, User, City])
		database.close()

	def test_create(self):
		#Testing creation of amenity
		rv = self.app.post("/amenities", data=amenity_1)
		self.assertEqual(rv.status_code, 201)
		self.assertEqual(json.loads(rv.data)['id'], 1)

		#Testing creation of amenity existing name
		rv = self.app.post("/amenities", data=amenity_1)
		self.assertEqual(rv.status_code, 409)

		#Testing creationg of amenity wiht no name field
		rv = self.app.post("/amenities", data=dict())
		self.assertEqual(rv.status_code, 400)

	def test_list(self):
		#Check that there are no amentities
		rv = self.app.get("/amenities")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)["data"]), 0)

		#Creating a new amenity
		rv = self.app.post('/amenities', data=amenity_1)
		self.assertEqual(rv.status_code, 201)

		#Test that new amenity is returned
		rv = self.app.get("/amenities")
		self.assertEqual(len(json.loads(rv.data)["data"]), 1)

	def test_get(self):
		#Creating amenity
		rv = self.app.post('/amenities', data=amenity_1)
		self.assertEqual(rv.status_code, 201)

		#Testing that amenity is returned
		rv = self.app.get('/amenities/1')
		self.assertEqual(rv.status_code, 200)

		#Test that that I cant get returned data from invalid id
		rv = self.app.get("/amenities/123")
		self.assertEqual(rv.status_code, 404)

	def test_delete(self):
		#Creating amenity
		rv = self.app.post('/amenities', data=amenity_1)
		self.assertEqual(rv.status_code, 201)

		#Testing that amenity was created and returned
		rv = self.app.get('/amenities')
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)), 1)	

		#Deleting amenity
		rv = self.app.delete('/amenities/1')
		self.assertEqual(rv.status_code, 200)

		#Checking amenity was deleted
		rv = self.app.get('/amenities')
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)["data"]), 0)

		#Testing to see if I can delete non-existent amenity
		rv = self.app.delete('/amenities/123')
		self.assertEqual(rv.status_code, 404)

	def test_create_place_amenity(self):
		#Creating amenity
		rv = self.app.post('/users', data=user_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/states', data=state_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/states/1/cities', data=city_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/places', data=place_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/amenities', data=amenity_1)
		self.assertEqual(rv.status_code, 201)

		#Testing creating a new amenity for a place
		rv = self.app.post('/places/1/amenities/1')
		self.assertEqual(rv.status_code, 201)

		#Testing for 404 if place does not exist
		rv = self.app.post('/places/404/amenities/1')
		self.assertEqual(rv.status_code, 404)

		#Testing for 404 if amenity does not exist
		rv = self.app.post('/places/1/amenities/404')
		self.assertEqual(rv.status_code, 404)

			#Testing to see if I can create a duplicate amenity for a place
		rv = self.app.post('/places/1/amenities/1')
		self.assertEqual(rv.status_code, 400)

	def test_get_place_amenity(self):
		#Creating amenity
		rv = self.app.post('/users', data=user_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/states', data=state_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/states/1/cities', data=city_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/places', data=place_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/amenities', data=amenity_1)
		self.assertEqual(rv.status_code, 201)

		#Testing there are no amenities for a place
		rv = self.app.get('/places/1/amenities')
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)['data']), 0)

		#Testing creation of new amenity for place
		rv = self.app.post('/places/1/amenities/1')
		self.assertEqual(rv.status_code, 201)

		#Testing that there is one amenity for a place
		rv = self.app.get('/places/1/amenities')
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)['data']), 1)

		#Testing for 404 if the place does not exist
		rv = self.app.get('/places/404/amentities')
		self.assertEqual(rv.status_code, 404)

	def test_delete_place_amenity(self):
		#Creating amenity for place
		rv = self.app.post('/users', data=user_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/states', data=state_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/states/1/cities', data=city_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/places', data=place_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/amenities', data=amenity_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/places/1/amenities/1')
		self.assertEqual(rv.status_code, 201)

		#Ensuring there is a amenity for place
		rv = self.app.get('/places/1/amenities')
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)['data']), 1)

		#Deleting amenity
		rv = self.app.delete('/places/1/amenities/1')
		self.assertEqual(rv.status_code, 200)

		#Ensuring place was deleted
		rv = self.app.get('/places/1/amenities')
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)['data']), 0)

		#Testing for 404 if place does not exist
		rv = self.app.delete('/places/404/amenities/1')
		self.assertEqual(rv.status_code, 404)

		#Testing for 404 if amenity does not exist
		rv = self.app.delete('/places/1/amenities/404')
		self.assertEqual(rv.status_code, 404)
