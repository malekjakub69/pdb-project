from src.models.article import Article
from src.models.user import User
from src.models.read import Read
from flask_restful import Resource, request
from werkzeug.exceptions import NotFound, BadRequest
from src.broker.wrapper import TransferObject
from src.broker.broker import publish_to_queue
import json

class SQLReadResource(Resource):
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

        if Read.query.filter_by(user_id=data["user_id"], article_id=data["article_id"]).first():
            return ({"message": "already_read"}, 208)

        read = Read(
            user=user,
            article=article,
        )
        read.save()

        transfer = {
            "id": read.id,
            "timestamp": read.timestamp.strftime("%m/%d/%Y, %H:%M:%S"),
            "type": 1,
            "user_id": read.user_id,
            "article_id": read.article_id,
            "region_id": read.user.region_id,
            "tags": json.loads(read.article.tags) if read.article.tags else []
        }
        transfer_object = TransferObject('insert', 'read', transfer)
        publish_to_queue(transfer_object.to_dict(), 'read')

        return ({"message": "read"}, 201)
