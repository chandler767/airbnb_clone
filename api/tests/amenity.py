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
		rv = self.app.post("/amentities", data=dict())
		self.assertEqual(rv.status_code, 400)

	def test_list(self):
		#Check that there are no amentities
		rv = self.app.get("/amenities")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)), 0)

		#Creating a new amenity
		rv = self.app.post('/amenities', data=amenity_1)
		self.assertEqual(rv.status_code, 201)

		#Test that new amenity is returned
		rv = self.app.get("/amenities")
		self.assertEqual(len(json.loads(rv.data)), 1)

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
		self.assertEqual(len(json.loads(rv.data)), 0)

		#Testing to see if I can delete non-existent amenity
		rv = self.app.delete('/amenities/123')
		self.assertEqual(rv.status_code, 404)