from app import app
from app.views import user
from app.models.user import User
from app.models.base import database
from datetime import datetime, timedelta
import unittest
import json
import logging

user_1 = dict(first_name="Jon", last_name="Snow", email="jon@snow.com", password="toto1234")
user_2 = dict(last_name="Snow", email="jon2@snow.com", password="testpw")
user_3 = dict(first_name="Jon", email="jon3@snow.com", password="testpw")
user_4 = dict(first_name="Jon", last_name="Snow", password="toto1234")
user_5 = dict(first_name="Jon", last_name="Snow", email="jon4@snow.com")

class UserUnitTest(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		logging.disable(logging.CRITICAL)

		database.connect()
		database.create_tables([User], safe=True)

	def tearDown(self):
		database.drop_tables([User])
		database.close()

	def test_create(self):
		#Testing the creation of a new user
		rv = self.app.post("/users", data=user_1)
		self.assertEqual(rv.status_code, 201)
		self.assertEqual(json.loads(rv.data)["id"], 1)

		#Testing for missing first name
		rv = self.app.post("/users", data=user_2)
		self.assertEqual(rv.status_code, 400)

		#Testing for missing last name
		rv = self.app.post("/users", data=user_3)
		self.assertEqual(rv.status_code, 400)

		#Testing for missing email
		rv = self.app.post("/users", data=user_4)
		self.assertEqual(rv.status_code, 400)

		#Testing for missing password
		rv = self.app.post("/users", data=user_5)
		self.assertEqual(rv.status_code, 400)

		#Testing if users can have the same email
		rv = self.app.post("/users", data=user_1)
		self.assertEqual(rv.status_code, 409)

	def test_list(self):
		#Test that no users exist
		rv = self.app.get("/users")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)["data"]), 0) #

		#Creating user
		rv = self.app.post("/users", data=user_1)
		self.assertEqual(rv.status_code, 201)

		#Testing that one user is returned
		rv = self.app.get("/users")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)["data"]), 1)#

	def test_get(self):
		#Creating user
		rv = self.app.post("/users", data=user_1)
		self.assertEqual(rv.status_code, 201)
		created_data = json.loads(rv.data)

		#Get created user
		rv = self.app.get("/users/1")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(created_data["email"], json.loads(rv.data)["email"])

		#Check if user does not exist
		rv = self.app.get("/users/123")
		self.assertEqual(rv.status_code, 404)

	def test_delete(self):
		#Create user
		rv = self.app.post("/users", data=user_1)
		self.assertEqual(rv.status_code, 201)

		#Testing that user was created and returned
		rv = self.app.get('/users')
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)["data"]), 1)#

		#Testing deletion of a user
		rv = self.app.delete('/users/1')
		self.assertEqual(rv.status_code, 200)

		#Testing that user was deleted
		rv = self.app.get('/users')
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)["data"]), 0)

		#Test that I cant delete a fake user
		rv = self.app.delete('/users/123')
		self.assertEqual(rv.status_code, 404)

	def test_update(self):
		#Creating user
		rv = self.app.post("/users", data=user_1)
		self.assertEqual(rv.status_code, 201)

		#Testing updating first name
		rv = self.app.put('/users/1', data=dict(first_name='Arya'))
		self.assertEqual(rv.status_code, 200)

		#Testing updating last name
		rv = self.app.put('/users/1', data=dict(last_name='Lannister'))
		self.assertEqual(rv.status_code, 200)

		#Testing updating admin configuration
		rv = self.app.put('/users/1', data=dict(is_admin=True))
		self.assertEqual(rv.status_code, 200)

		#Testing updating password
		update_time = datetime.now()
		rv = self.app.put('/users/1', data=dict(password='newpassword'))
		self.assertEqual(rv.status_code, 200)

		#Testing updating email
		rv = self.app.put('/users/1', data=dict(email='arya@stark.com'))
		self.assertEqual(rv.status_code, 400)

		#Testing that update time is correct
		rv = self.app.get('/users/1')
		self.assertEqual(rv.status_code, 200)
		self.assertTrue(abs(datetime.strptime(json.loads(rv.data)['updated_at'],"%Y/%m/%d %H:%M:%S") - update_time) < timedelta(seconds=3))

		#Checking that updates happend
		rv = self.app.get('/users/1')
		self.assertEqual(rv.status_code, 200)
		data = json.loads(rv.data)
		self.assertEqual(data['email'], user_1['email'])
		self.assertEqual(data['first_name'], "Arya")
		self.assertEqual(data['last_name'], "Lannister")
		self.assertEqual(data['is_admin'], True)

		#Testing update for invalid user
		rv = self.app.put('/users/123', data=dict(first_name='Jon'))
		self.assertEqual(rv.status_code, 404)

if __name__ == "__main__":
	unittest.main()
