from app import app
from app.models.user import User
from app.models.place import Place
from app.models.base import database
from app.models.review import Review
from app.models.review_user import ReviewUser
from app.models.review_place import ReviewPlace
from app.models.state import State
from app.models.city import City

import unittest 
import json
import logging

from user import user_1
from place import place_1
from state import state_1
from city import city_1

review_1 = dict(message="review message", user_id=1, stars=5)
review_2 = dict(message="review message", stars=5)
review_3 = dict(user_id=1)
review_4 = dict(message="review message", user_id="1", stars=5)
review_5 = dict(message=2, user_id=1)
review_6 = dict(message="review message", user_id=1, stars="5")

class ReviewUnitTest(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		logging.disable(logging.CRITICAL)

		database.connect()
		database.create_tables([User, State, City, Place, Review, ReviewUser, ReviewPlace], safe=True)

		#Creating user
		rv = self.app.post("/users", data=user_1)
		self.assertEqual(rv.status_code, 201)

	def tearDown(self):
		database.drop_tables([User, State, City, Place, Review, ReviewUser, ReviewPlace])
		database.close()

	def test_create_user(self):
		#Creating review
		rv = self.app.post('/users/1/reviews', data=review_1)
		self.assertEqual(rv.status_code, 201)
		self.assertEqual(json.loads(rv.data)['id'], 1)

		#Creating review for user that does no exist
		rv = self.app.post('/users/123/reviews', data=review_1)
		self.assertEqual(rv.status_code, 404)

		#Testing missing user_id 
		rv = self.app.post('/users/1/reviews', data=review_2)
		self.assertEqual(rv.status_code, 400)

		#Testing missing message
		rv = self.app.post('/users/1/reviews', data=review_3)
		self.assertEqual(rv.status_code, 400)

		#Testing with different user_id type
		rv = self.app.post("/users/1/reviews", data=review_4)
		self.assertEqual(rv.status_code, 201)

		#Testing with different message type
		rv = self.app.post("/users/1/reviews", data=review_5)
		self.assertEqual(rv.status_code, 201)

		#Testing with different star data type
		rv = self.app.post("/users/1/reviews", data=review_6)
		self.assertEqual(rv.status_code, 201)

	def test_list(self):
		#Testing that there are no reviews returned
		rv = self.app.get("/users/1/reviews")
		self.assertEqual(len(json.loads(rv.data)), 0)

		#Creating review
		rv = self.app.post('/users/1/reviews', data=review_1)
		self.assertEqual(rv.status_code, 201)
		self.assertEqual(json.loads(rv.data)['id'], 1)

		#Testing that review is returned
		rv = self.app.get("/users/1/reviews")
		self.assertEqual(len(json.loads(rv.data)), 1)

		#Testing getting reviews for invalid user
		rv = self.app.get("/users/123/reviews")
		self.assertEqual(rv.status_code, 404)

	def test_get(self):
		#Testing getting review with invalid review id
		rv = self.app.get("/users/1/123")
		self.assertEqual(rv.status_code, 404)

		#Testing getting review with invalid user id
		rv = self.app.get("/users/123/1")
		self.assertEqual(rv.status_code, 404)

		#Creating review
		rv = self.app.post('/users/1/reviews', data=review_1)
		self.assertEqual(rv.status_code, 201)

		#Getting review
		rv = self.app.get("/users/1/1")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(json.loads(rv.data)["id"], 1)

	def test_delete(self):
		#Testing deletion of review with invalid review id
		rv = self.app.delete("/users/1/123")
		self.assertEqual(rv.status_code, 404)

		#Testing deletion of review with invalid user id
		rv = self.app.delete("/users/123/1")
		self.assertEqual(rv.status_code, 404)

		#Creating review
		rv = self.app.post('/users/1/reviews', data=review_1)
		self.assertEqual(rv.status_code, 201)

		#Ensuring review was created 
		rv = self.app.get("/users/1/reviews")
		self.assertEqual(len(json.loads(rv.data)), 1)

		#Deleting review
		rv = self.app.delete("/users/1/1")
		self.assertEqual(rv.status_code, 200)

		#Ensuring review was deleted
		rv = self.app.get("/users/1/reviews")
		self.assertEqual(len(json.loads(rv.data)), 0)

	def test_place_reviews(self):
		#Creating place
		rv = self.app.post('/states', data=state_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/states/1/cities', data=city_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post("/places", data=place_1)
		self.assertEqual(rv.status_code, 201)

		#Testing getting review of place with invalid id
		rv = self.app.get("/places/123/reviews")
		self.assertEqual(rv.status_code, 404)

		#Testing that there are no reviews for the place
		rv = self.app.get("/places/1/reviews")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)), 0)

		#Creating review at place
		rv = self.app.post("/places/1/reviews", data=review_1)
		self.assertEqual(rv.status_code, 201)

		#Testing returning of review at place
		rv = self.app.get("/places/1/reviews")
		self.assertEqual(rv.status_code, 200)
		self.assertEqual(len(json.loads(rv.data)), 1)

	def test_create_place_reviews(self):
		#Creating place
		rv = self.app.post('/states', data=state_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/states/1/cities', data=city_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post("/places", data=place_1)
		self.assertEqual(rv.status_code, 201)

		#Creating review with invalid place id
		rv = self.app.post("/places/123/reviews")
		self.assertEqual(rv.status_code, 404)

		#Testing missing user_id 
		rv = self.app.post('/places/1/reviews', data=review_2)
		self.assertEqual(rv.status_code, 400)

		#Testing missing message
		rv = self.app.post('/places/1/reviews', data=review_3)
		self.assertEqual(rv.status_code, 400)

		#Testing with different user_id type
		rv = self.app.post("/places/1/reviews", data=review_4)
		self.assertEqual(rv.status_code, 201)

		#Testing with different message type
		rv = self.app.post("/places/1/reviews", data=review_5)
		self.assertEqual(rv.status_code, 201)

		#Testing with different star data type
		rv = self.app.post("/places/1/reviews", data=review_6)
		self.assertEqual(rv.status_code, 201)

		#Testing creation of review
		rv = self.app.post('/places/1/reviews', data=review_1)
		self.assertEqual(rv.status_code, 201)

	def test_get_place_review(self):
		#Creating place
		rv = self.app.post('/states', data=state_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/states/1/cities', data=city_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post("/places", data=place_1)
		self.assertEqual(rv.status_code, 201)

		#Creating review 
		rv = self.app.post('/places/1/reviews', data=review_1)
		self.assertEqual(rv.status_code, 201)

		#Testing that review is returned
		rv = self.app.get("/places/1/1")
		self.assertEqual(rv.status_code, 200)

		#Testing getting review of invalid place id
		rv = self.app.get("/places/123/1")
		self.assertEqual(rv.status_code, 404)

		#Testing getting review of invalid review id
		rv = self.app.get("/places/1/123")
		self.assertEqual(rv.status_code, 404)


	def test_delete_place_review(self):
		#Creating place
		rv = self.app.post('/states', data=state_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/states/1/cities', data=city_1)
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post("/places", data=place_1)
		self.assertEqual(rv.status_code, 201)

		#Testing deletion of review with invalid place id 
		rv = self.app.delete("/places/123/1")
		self.assertEqual(rv.status_code, 404)

		#Testing deletion of review with inavalid review id
		rv = self.app.delete("/places/1/123")
		self.assertEqual(rv.status_code, 404)

		#Creating review
		rv = self.app.post('/places/1/reviews', data=review_1)
		self.assertEqual(rv.status_code, 201)

		#Ensuring review was created 
		rv = self.app.get("/places/1/reviews")
		self.assertEqual(len(json.loads(rv.data)), 1)

		#Deleting review
		rv = self.app.delete("/places/1/1")
		self.assertEqual(rv.status_code, 200)

		#Ensuring review was deleted
		rv = self.app.get("/places/1/reviews")
		self.assertEqual(len(json.loads(rv.data)), 0)
