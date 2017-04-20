from app import app
from app.models.base import database
from app.models.state import State
import json
import unittest
import logging

state_1 = dict(name="Virginia")
state_2 = dict()

class StateUnitTest(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		logging.disable(logging.CRITICAL)

		database.connect()
		database.create_tables([State], safe=True)

	def tearDown(self):
		database.drop_tables([State])
		database.close()

	def test_create(self):
		#Testing creation of a state
		rv = self.app.post("/states", data=state_1)
		self.assertEqual(rv.status_code, 201)
		self.assertEqual(json.loads(rv.data)["id"], 1)

		#Testing creation of state with no name
		rv = self.app.post("/states", data=state_2)
		self.assertEqual(rv.status_code, 400)

		#Testing creationg of state with duplicate name
		rv = self.app.post("/states", data=state_1)
		self.assertEqual(rv.status_code, 409)

	def test_list(self):
		#Test that there are no states
		rv = self.app.get("/states")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)["data"]), 0) 

		#Creating state
		rv = self.app.post("/states", data=state_1)
		self.assertEqual(rv.status_code, 201)

		#Test that there is one state returned
		rv = self.app.get("/states")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)["data"]), 1)

	def test_get(self):
		#Creating state
		rv = self.app.post("/states", data=state_1)
		self.assertEqual(rv.status_code, 201)

		#Test that created state is returned
		rv = self.app.get("/states/1")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(json.loads(rv.data)["name"], "Virginia")

		#Test for state that does not exist
		rv = self.app.get("/states/123")
		self.assertEqual(rv.status_code, 404)

	def test_delete(self):
		#Creating state
		rv = self.app.post("/states", data=state_1)
		self.assertEqual(rv.status_code, 201)

		#Testing that state was created and returned
		rv = self.app.get('/states')
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)["data"]), 1)#

		#Testing deletion of a state
		rv = self.app.delete('/states/1')
		self.assertEqual(rv.status_code, 200)

		#Testing that state was deleted
		rv = self.app.get('/states')
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)["data"]), 0)

		#Test that I cant delete a fake state
		rv = self.app.delete('/states/123')
		self.assertEqual(rv.status_code, 404)

