from src.models.article import Article
from src.models.user import User
from src.models.like import Like
from flask_restful import Resource, request
from werkzeug.exceptions import NotFound, BadRequest
from src.broker.wrapper import TransferObject
from src.broker.broker import publish_to_queue
import json

class SQLLikeResource(Resource):
    def post(self):
        data = request.get_json()

        if not data["user_id"]:
            raise BadRequest("user_id_required")
        if not (user := User.get_by_id(data["user_id"])):
            raise NotFound("entity_not_found")
        if not data["article_id"]:
            raise BadRequest("article_id_required")
        if not (article := Article.get_by_id(data["article_id"])):
            raise NotFound("entity_not_found")

        if Like.query.filter_by(user_id=data["user_id"], article_id=data["article_id"]).first():
            raise BadRequest("article_already_liked")

        like = Like(
            user=user,
            article=article,
        )
        like.save()

        transfer = {
            "id": like.id,
            "timestamp": like.timestamp.strftime("%m/%d/%Y, %H:%M:%S"),
            "type": 0,
            "user_id": like.user_id,
            "article_id": like.article_id,
            "region_id": like.user.region_id,
            "tags": json.loads(like.article.tags) if like.article.tags else []
        }
        transfer_object = TransferObject('insert', 'like', transfer)
        publish_to_queue(transfer_object.to_dict(), 'like')

        return ({"message": "article_liked"}, 201)


class SQLUnlikeResource(Resource):
    def post(self):
        data = request.get_json()

        if not data["user_id"]:
            raise BadRequest("user_id_required")
        if not (user := User.get_by_id(data["user_id"])):
            raise NotFound("entity_not_found")
        if not data["article_id"]:
            raise BadRequest("article_id_required")
        if not (Article.get_by_id(data["article_id"])):
            raise NotFound("entity_not_found")

        if not (like := Like.query.filter_by(user_id=data["user_id"], article_id=data["article_id"]).first()):
            raise BadRequest("article_not_liked")

        like.delete()

        transfer_object = TransferObject('delete', 'like', like.get_full_dict())
        publish_to_queue(transfer_object.to_dict(), 'like')

        return ({"message": "article_unliked"}, 201)
