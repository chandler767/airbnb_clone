import peewee
import datetime
from config import DATABASE

database = peewee.MySQLDatabase(database=DATABASE["database"], host=DATABASE["host"], user=DATABASE["user"], port=DATABASE["port"], passwd=DATABASE["password"], charset=DATABASE["charset"])

class BaseModel(peewee.Model):
	id = peewee.PrimaryKeyField(unique=True)
	created_at = peewee.DateTimeField(default=datetime.datetime.now(),formats="%Y/%m/%d %H:%M:%S")
	updated_at = peewee.DateTimeField(default=datetime.datetime.now(),formats="%Y/%m/%d %H:%M:%S")

	# updates updated_at before saving
	def save(self, *args, **kwargs):
		self.updated_at = datetime.datetime.now()
		super(BaseModel, self).save(*args, **kwargs)

	class Meta:
		# connects to database
		database = database
		order_by = ("id", )