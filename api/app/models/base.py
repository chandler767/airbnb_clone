import peewee, datetime, sys
sys.path.append("....")
from config import *

# variable database linked to DATABASE imported from config file

database = peewee.MySQLDatabase(database=DATABASE["database"], host=DATABASE["host"], user=DATABASE["user"], port=DATABASE["port"], passwd=DATABASE["password"], charset=DATABASE["charset"])

class BaseModel(peewee.Model):
	id = peewee.PrimaryKeyField(unique=True)
	created_at = peewee.DateTimeField(default=datetime.datetime.now())
	updated_at = peewee.DateTimeField(default=datetime.datetime.now())

	# overloads save method of Model to update updated_at before saving
	def save(self, *args, **kwargs):
		self.updated_at = datetime.datetime.now()
		return super(BaseModel, self).save(*args, **kwargs)

	class Meta:
		# connects to database
		database = database
		order_by = ("id", )