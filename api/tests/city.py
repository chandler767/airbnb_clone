from app import app
from app.models.base import database
from app.models.city import City
from app.models.state import State
import json
import unittest
import logging

state_1 = dict(name="Virginia")
state_2 = dict()

city_1 = dict(name="Test")
city_2 = dict()

class CityUnitTest(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		logging.disable(logging.CRITICAL)

		database.connect()
		database.create_tables([City, State], safe=True)

		rv = self.app.post("/states", data=state_1)
		self.assertEqual(rv.status_code, 201)

	def tearDown(self):
		database.drop_tables([City, State])
		database.close()

	def test_create(self):
		#Testing the creation of a City
		rv = self.app.post("/states/1/cities", data=city_1)
		self.assertEqual(rv.status_code, 201)
		self.assertEqual(json.loads(rv.data)["id"], 1)

		#Testing for missing name when creating city
		rv = self.app.post("/states/1/cities", data=city_2)
		self.assertEqual(rv.status_code, 400)

		#Testing creating duplicate city
		rv = self.app.post("/states/1/cities", data=city_1)
		self.assertEqual(rv.status_code, 409)

	def test_list(self):
		#Test that there are no cities
		rv = self.app.get("/states/1/cities")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)['data']), 0) 

		#Creating city
		rv = self.app.post("/states/1/cities", data=city_1)
		self.assertEqual(rv.status_code, 201)

		#Test that there is one city returned
		rv = self.app.get("/states/1/cities")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)['data']), 1)

	def test_get(self):
		#Creating city
		rv = self.app.post("/states/1/cities", data=city_1)
		self.assertEqual(rv.status_code, 201)

		#Test that created city is returned
		rv = self.app.get("/states/1/cities/1")
		self.assertEqual(rv.status_code, 200)

		#Test for city that does not exist
		rv = self.app.get("/states/1/cities/123")
		self.assertEqual(rv.status_code, 404)

	def test_delete(self):
		#Creating city
		rv = self.app.post("/states/1/cities", data=city_1)
		self.assertEqual(rv.status_code, 201)

		#Testing that city was created and returned
		rv = self.app.get('/states/1/cities')
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)['data']), 1)

		#Testing deletion of a city
		rv = self.app.delete('/states/1/cities/1')
		self.assertEqual(rv.status_code, 200)

		#Testing that state was deleted
		rv = self.app.get('/states/1/cities')
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)['data']), 0)

		#Test that I cant delete a fake state
		rv = self.app.delete('/states/1/cities/123')
		self.assertEqual(rv.status_code, 404)


