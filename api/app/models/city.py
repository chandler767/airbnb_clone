from peewee import *
from base import BaseModel
from state import State

class City(BaseModel):
	name = CharField(128, null=False)
	state = ForeignKeyField(State, related_name="cities", on_delete="CASCADE")

	# returns hash of all class attributes, inc. inherited ones
	def to_dict(self):
		state = State.get(State.id == self.state)

		return {	'id': self.id,
					'created_at': self.created_at.strftime('%Y/%m/%d %H:%M:%S'),
					'updated_at': self.updated_at.strftime('%Y/%m/%d %H:%M:%S'),
					'name': self.name,
					'state_id': state.id 	}