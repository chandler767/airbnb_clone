from peewee import *
from base import BaseModel

class Amenity(BaseModel):
	name = CharField(128, null=False)

	# returns hash of all class attributes, inc. inherited ones
	def to_dict(self):
		return {	'id': self.id,
					'created_at': self.created_at.strftime('%Y/%m/%d %H:%M:%S'),
					'updated_at': self.updated_at.strftime('%Y/%m/%d %H:%M:%S'),
					'name': self.name	}