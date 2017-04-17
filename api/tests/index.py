import os
import unittest
import tempfile
import json
from app import app
from app.views import index
from datetime import datetime

class UnitTest(unittest.TestCase):

	def setUp(self):
		self.app = app.test_client()

	def test_200(self):
		rv = self.app.get('/')
		self.assertEqual(rv.status_code, 200)

	def test_status(self):
		rv = self.app.get('/')
		self.assertEqual(json.loads(rv.data)["status"], 'OK')

	def test_time(self):
		rv = self.app.get('/')
		data = str(json.loads(rv.data)['time'])
		time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		self.assertEqual(data, time_now)

	def test_time_utc(self):
		rv = self.app.get('/')
		data = str(json.loads(rv.data)["utc_time"])
		time_now = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
		self.assertEqual(data, time_now)

if __name__ == '__main__':
    unittest.main()