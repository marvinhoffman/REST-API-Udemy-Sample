from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class ItemList(Resource):
	@jwt_required()
	def get(self):
		return {'items': [item.json() for item in ItemModel.query.all()]} # List Comprehension, more pythonesque
		# return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))} # lambda, more universal


class Item(Resource):
	# class blocks:
	# parser code
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type=float,
		required=True,
		help="This field cannot be left blank."
	)
	parser.add_argument('store_id',
		type=int,
		required=True,
		help="Every item needs a store id."
	)

	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()

		return {'message': 'No item found.'}, 404


	# @jwt_required()
	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message': 'Item already exists.'},400

		data = Item.parser.parse_args()
		item = ItemModel(name, **data) # **data translates to data['price'], data['store_id']

		try:
			item.save_to_db()
		except:
			return {'message': 'An error has occurred inserting the item.'}, 500

		return item.json(), 201


	# @jwt_required()
	def put(self, name):
		data = Item.parser.parse_args()

		item = ItemModel.find_by_name(name)
		
		if item is None:
			item = item = ItemModel(name, **data) # **data translates to data['price'], data['store_id']
			status_code = 201
		else:
			item.price = data['price']
			item.store_id = data['store_id']
			status_code = 200

		item.save_to_db()

		return item.json(), status_code


	# @jwt_required()
	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()

		return {'message': 'Item Deleted.'}



