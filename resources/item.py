from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint('items', __name__, description='Operations on items')


@blp.route('/item/<string:item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item: ItemModel = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item: ItemModel = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()

        current_app.logger.info(
            f'Item deleted successfully: [{item.id}] {item.name} '
            f'(${item.price})')

        return {'message': 'Item deleted successfully.'}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item: ItemModel = ItemModel.query.get(item_id)
        if item:
            item.price = item_data['price']
            item.name = item_data['name']

            current_app.logger.info(
                f'Item updated successfully: [{item.id}] {item.name} '
                f'(${item.price})')
        else:
            item = ItemModel(id=item_id, **item_data)
            current_app.logger.info(
                f'Item created successfully: [{item.id}] {item.name} '
                f'(${item.price})')

        db.session.add(item)
        db.session.commit()

        return item


@blp.route('/item')
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
            current_app.logger.info(
                f'Item created successfully: [{item.id}] {item.name} '
                f'(${item.price})')
        except SQLAlchemyError:
            current_app.logger.info(
                f'Item created successfully: [{item.id}] {item.name} '
                f'(${item.price})')
            abort(500, message='An error occurred while adding the item.',
                  logger=current_app.logger)

        return item, 201
