from peewee import *
from base import BaseModel
from user import User

class Review(BaseModel):
	message = TextField(null=False)
	stars = IntegerField(default=0)
	user = ForeignKeyField(User, related_name="reviews", on_delete="CASCADE")

	def to_dict(self):
		from review_user import ReviewUser
		from review_place import ReviewPlace

		data = {"id": self.id,
				"created_at": self.created_at,
				"updated_at": self.updated_at,
				"message": self.message,
				"stars": self.stars,
				"from_user_id": self.user.id}

		try:
			review_user = ReviewUser.get(ReviewUser.review == self.id)
			data["to_user_id"] = review_user.user.id

		except:
			data["to_user_id"] = None

		try:
			review_place = ReviewPlace.get(ReviewPlace.review == self.id)
			data["to_place_id"] = review_place.place.id

		except:
			data["to_place_id"] = None

		return data