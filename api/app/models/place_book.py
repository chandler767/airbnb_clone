from peewee import *
from base import BaseModel
from place import Place
from user import User

class PlaceBook(BaseModel):
	place = ForeignKeyField(rel_model=Place)
	user = ForeignKeyField(rel_model=User, related_name="places_booked")
	is_validated = BooleanField(default=False)
	date_start = DateTimeField(null=False, formats="%d/%m/%Y %H:%M:%S")
	number_nights = IntegerField(default=1)

	# returns hash of all class attributes, inc. inherited ones
	def to_hash(self):
		place = Place.get(Place.id == self.place)
		user = User.get(User.id == self.user)
		data =  {	'id': self.id,
					'created_at': self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
					'updated_at': self.updated_at.strftime('%d/%m/%Y %H:%M:%S'),
					'place_id': self.place,
					'user_id': self.user,
					'is_validated': self.is_validated,
					'date_start': self.date_start,
					'number_nights': self.number_nights	}

		return super(PlaceBook, self).to_dict(self, data)