from peewee import *
from base import BaseModel

class State(BaseModel):
	name = CharField(128, null=False, unique=True)

	# returns hash of all class attributes, inc. inherited ones
	def to_hash(self):
		return {	'id': self.id,
					'created_at': self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
					'updated_at': self.updated_at.strftime('%d/%m/%Y %H:%M:%S'),
					'name': self.name	}