from app import app
from flask import request
from flask_json import json_response
from app.models.base import database
from app.models.user import User
from peewee import *
from flask import jsonify
from return_styles import ListStyle

@app.route("/users", methods=["GET", "POST"])
def users():
	if request.method == "POST":
		try:
			if "email" not in request.form or "password" not in request.form or "first_name" not in request.form or "last_name" not in request.form:
				return json_response(status_=400, code=40000, msg="missing parameters")
				
			new_user = User(email=request.form["email"],
							password=request.form["password"],
							first_name=request.form["first_name"],
							last_name=request.form["last_name"])
			new_user.save()
			return jsonify(new_user.to_dict()), 201

		except IntegrityError:
			return json_response(status_=409,
								msg="Email already exists",
								code=10000)

	elif request.method == "GET":
		query = User.select()

		return ListStyle.list(query, request), 200

@app.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"])
def users_id(user_id):
	if request.method == "GET":
		try:
			query = User.get(User.id == user_id)
			return jsonify(query.to_dict()), 200

		except User.DoesNotExist:
			return json_response(status_=404, msg="not found")

	elif request.method == "PUT":
		try:
			query = User.get(User.id == user_id)

			for key in request.form:
				if key == "last_name":
					query.last_name = str(request.form[key])

				elif key == "first_name":
					query.first_name = str(request.form[key])

				elif key == "is_admin":
					query.is_admin = str(request.form[key])

				elif key == "password":
					query.password = str(request.form[key])
					
				elif key == "email":
					return json_response(status_=400, msg="not allowed to update email")

			query.save()
			return jsonify(query.to_dict()), 200

		except User.DoesNotExist:
			return json_response(status_=404, msg="not found")

	elif request.method == "DELETE":
		try:
			user = User.get(User.id == user_id)
			user.delete_instance()
			user.save()
			
			return json_response(status_=200, msg="Success")

		except User.DoesNotExist:
			return json_response(status_=404, msg="not found")
