from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint('items', __name__, description='Operations on items')


@blp.route('/item/<int:item_id>')
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item: ItemModel = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        current_app.logger.info(f'jwt: {jwt}')
        if not jwt.get('is_admin'):
            abort(401, message='Admin privilege required.')

        item: ItemModel = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()

        current_app.logger.info(
            f'Item deleted successfully: [{item.id}] {item.name} '
            f'(${item.price})')

        return {'message': 'Item deleted successfully.'}

    @jwt_required()
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
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required(fresh=True)
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
        except IntegrityError:
            db.session.rollback()
            abort(409, message=f'Item already exists: {item_data}')
        except SQLAlchemyError as e:
            current_app.logger.info(
                f'Item created successfully: [{item.id}] {item.name} '
                f'(${item.price})')
            db.session.rollback()
            abort(500, message=f'An error occurred while adding the item: {e}')

        return item, 201
