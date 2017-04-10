from app.models.amenity import Amenity
from app.models.city import City
from app.models.place import Place
from app.models.place_amenity import PlaceAmenities
from app.models.place_book import PlaceBook
from app.models.state import State
from app.models.user import User
from app.models.base import database

# generates every table in the database
database.connect()
database.create_tables([
	Amenity, 
	City, 
	Place, 
	PlaceAmenities, 
	PlaceBook, 
	State, 
	User])
database.close()