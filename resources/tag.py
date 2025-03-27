from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema


blp = Blueprint('tags', __name__, description='Operations on tags')


@blp.route('/store/<int:store_id>/tag')
class TagInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            current_app.logger.error(
                f'An error occurred while adding a tag to store [{store_id}]: '
                f'{str(e)}')
            abort(
                500,
                message=str(e)
            )

        return tag


@blp.route('/item/<int:item_id>/tag/<int:tag_id>')
class LinkTagToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                500,
                message='An error occurred while linking the tag to the item.')

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                500,
                message='An error occurred while unlinking the '
                'tag to the item.')

        return {'message': 'Item removed from tag', 'item': item, 'tag': tag}


@blp.route('/tag/<int:tag_id>')
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(
        202,
        description='Delete a tag if no items are linked to it.',
        example={'message': 'Tag deleted successfully.'})
    @blp.response(
        400,
        description='Tag is linked to items.',
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            try:
                db.session.delete(tag)
                db.session.commit()
            except SQLAlchemyError:
                abort(
                    500,
                    message='An error occurred while deleting the tag.')
        abort(
            400,
            message='Tag is linked to items.'
        )
