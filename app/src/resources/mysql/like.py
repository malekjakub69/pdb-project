from src.models.article import Article
from src.models.user import User
from src.models.like import Like
from flask_restful import Resource, request
from werkzeug.exceptions import NotFound, BadRequest


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

        return ({"message": "article_unliked"}, 201)
