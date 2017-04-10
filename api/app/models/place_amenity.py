import peewee
from base import database
from place import Place
from amenity import Amenity

class PlaceAmenities(peewee.Model):
	place = peewee.ForeignKeyField(Place)
	amenity = peewee.ForeignKeyField(Amenity)

	class Meta:
		database = database