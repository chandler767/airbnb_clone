from peewee import *
from base import BaseModel
import hashlib

class User(BaseModel):
	email = CharField(128, null=False, unique=True)
	password = CharField(128, null=False)
	first_name = CharField(128, null=False)
	last_name = CharField(128, null=False)
	is_admin = BooleanField(default=False)

	# runs pswd parameter through md5 hash function and saves hash to self.password 
	def set_password(self, clear_password):
		m = hashlib.md5()
		self.password = m.update(clear_password)

	# returns hash of all class attributes, inc. inherited ones
	def to_hash(self):
		return {	'id': self.id,
					'created_at': self.created_at,
					'updated_at': self.updated_at,
					'email': self.email,
					'first_name': self.first_name,
					'last_name': self.last_name,
					'is_admin': self.is_admin 	}