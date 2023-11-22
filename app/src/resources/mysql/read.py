from src.models.article import Article
from src.models.user import User
from src.models.read import Read
from flask_restful import Resource, request
from werkzeug.exceptions import NotFound, BadRequest


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
            return ({}, 208)

        read = Read(
            user=user,
            article=article,
        )
        read.save()

        return ({"message": "readed"}, 201)
