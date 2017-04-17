from peewee import *
from base import BaseModel
import hashlib

class User(BaseModel):
	email = CharField(128, null=False, unique=True)
	password = CharField(128, null=False)
	first_name = CharField(128, null=False)
	last_name = CharField(128, null=False)
	is_admin = BooleanField(default=False)

	# runs password through md5 hash function and then sets hash to self.password
	def set_password(self, clear_password):
		m = md5()
		m.update(clear_password)
		self.password = m.hexdigest()

	# returns dict of all class attributes
	def to_hash(self):
		data = {	'id': self.id,
					'created_at': self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
					'updated_at': self.updated_at.strftime('%d/%m/%Y %H:%M:%S'),
					'email': self.email,
					'first_name': self.first_name,
					'last_name': self.last_name,
					'is_admin': self.is_admin 	}

		return data