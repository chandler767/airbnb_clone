from app import app 
from app.models.user import User
from app.models.review_user import ReviewUser
from app.models.review_place import ReviewPlace
from app.models.review import Review
from app.models.place import Place

from flask_json import json_response
from flask import jsonify, request

@app.route("/users/<user_id>/reviews", methods=["GET", "POST"])
def user_reviews(user_id):
	user_test = User.select().where(User.id == user_id)

	if user_test.wrapped_count() < 1:
		return json_response(status_=404, msg="user does not exist with that id")

	if request.method == "GET":
		reviews = []
		query = ReviewUser.select().where(ReviewUser.user == user_id) 

		for r in query:
			reviews.append(r.review.to_hash())

		return jsonify(reviews), 200


	elif request.method == "POST":
		if "message" not in request.form:
			return json_response(status_=400, msg="missing message field")

		elif "user_id" not in request.form:
			return json_response(status_=400, msg="missing user_id field")

		elif "stars" not in request.form:
			review = Review(message=str(request.form["message"]), user=request.form["user_id"])
			review.save()

			u_review = ReviewUser(user=user_id, review=review.id)
			u_review.save()

			return jsonify(review.to_hash()), 201

		else:
			review = Review(message=str(request.form["message"]), user=request.form["user_id"], stars=int(request.form["stars"]))
			review.save()

			u_review = ReviewUser(user=user_id, review=review.id)
			u_review.save()

			return jsonify(review.to_hash()), 201

@app.route("/users/<user_id>/<review_id>", methods=["GET", "DELETE"])
def user_review(user_id, review_id):
	user_test = User.select().where(User.id == user_id)

	if user_test.wrapped_count() < 1:
		return json_response(status_=404, msg="user does not exist with that id")

	review = Review.select().where(Review.id == review_id, Review.user == user_id)

	if review.wrapped_count() < 1:
		return json_response(status_=404, msg="no review with that id for user with selected id")

	if request.method == "GET":
		review = Review.get(Review.id == review_id, Review.user == user_id)
		return jsonify(review.to_hash()), 200

	elif request.method == "DELETE":
		ReviewUser.delete().where(ReviewUser.user == user_id, ReviewUser.review == review_id).execute()
		Review.delete().where(Review.id == review_id, Review.user == user_id).execute()
		return json_response(status_=200, msg="review deleted")

@app.route("/places/<place_id>/reviews", methods=["GET", "POST"])
def place_reviews(place_id):
	place_test = Place.select().where(Place.id == place_id)

	if place_test.wrapped_count() < 1:
		return json_response(status_=404, msg="place does not exist with that id")

	if request.method == "GET":
		reviews = []
		query = ReviewPlace.select().where(ReviewPlace.place == place_id) 

		for r in query:
			reviews.append(r.review.to_hash())

		return jsonify(reviews), 200

	elif request.method == "POST":
		if "message" not in request.form:
			return json_response(status_=400, msg="missing message field")

		elif "user_id" not in request.form:
			return json_response(status_=400, msg="missing user_id field")

		elif "stars" not in request.form:
			# if type(request.form["message"]) != str:
			# 	return json_response(status_=400, msg="invalid data type for message")

			# if type(request.form["user_id"] != int):
			# 	return json_response(status_=400, msg="invalid data type for user id")

			review = Review(message=str(request.form["message"]), user=request.form["user_id"])
			review.save()

			p_review = ReviewPlace(place=place_id, review=review.id)
			p_review.save()

			return jsonify(review.to_hash()), 201

		else:
			# if type(request.form["message"]) != str:
			# 	return json_response(status_=400, msg="invalid data type for message")

			# if type(request.form["user_id"] != int):
			# 	return json_response(status_=400, msg="invalid data type for user id")

			# if type(request.form["stars"] != int):
			# 	return json_response(status_=400, msg="invalid data type for stars")

			review = Review(message=str(request.form["message"]), user=request.form["user_id"], stars=int(request.form["stars"]))
			review.save()

			p_review = ReviewPlace(place=place_id, review=review.id)
			p_review.save()

			return jsonify(review.to_hash()), 201

@app.route("/places/<place_id>/<review_id>", methods=["GET", "DELETE"])
def place_review(place_id, review_id):
	query = ReviewPlace.select().where(ReviewPlace.review == review_id, ReviewPlace.place == place_id)

	if query.wrapped_count() < 1:
		return json_response(status_=404, msg="not found")

	if request.method == "GET":
		query = Review.get(Review.id == review_id)
		return jsonify(query.to_hash()), 200

	elif request.method == "DELETE":
		ReviewPlace.delete().where(ReviewPlace.review == review_id, ReviewPlace.place == place_id).execute()
		Review.delete().where(Review.id == review_id).execute()
		return json_response(status_=200, msg="review delete")
