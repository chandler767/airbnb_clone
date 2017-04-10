from app.models.base import database
from app.models.user import User
from app.models.city import City
from app.models.state import State
from app.models.place import Place
from app.models.place_book import PlaceBook
from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities
''' Initializes each table in the database '''
database.connect()
database.create_tables([User,State,City,Place,Amenity,PlaceBook,PlaceAmenities,Review,ReviewPlace,ReviewUser], safe=True)
database.close()