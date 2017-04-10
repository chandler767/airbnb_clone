from peewee import *
from base import BaseModel

class Amenity(BaseModel):
	name = CharField(128, null=False)

	# returns hash of all class attributes, inc. inherited ones
	def to_hash(self):
		return {	'id': self.id,
					'created_at': self.created_at,
					'updated_at': self.updated_at,
					'name': self.name	}