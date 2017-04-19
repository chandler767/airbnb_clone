from flask_json import jsonify

class ListStyle():
	@staticmethod
	def list(select, request):
		list_return = {
			"data": "No results",
			"paging": {
				"next": None,
				"previous": None
			}
		}
		page = 1
		number = 10

		if "page" in request.args:
			page = int(request.args['page'])

		if "number" in request.args:
			number = int(request.args['number'])

		if page != 1:
			list_return["paging"]['prev'] = str(request.base_url) + '?page=' + str(page - 1) + '&number=' + str(number)

		list_return["paging"]['next'] = str(request.base_url) + '?page=' + str(page + 1) + '&number=' + str(number)

		dicts = []

		for r in select.paginate(page, number):
			dicts.append(r.to_dict())

		list_return["data"] = dicts

		return jsonify(list_return)
