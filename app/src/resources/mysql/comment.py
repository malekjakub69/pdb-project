from src.models.article import Article
from src.models.user import User
from src.models.comment import Comment
from flask_restful import Resource, request
from werkzeug.exceptions import NotFound, BadRequest


class SQLCommentResource(Resource):
    def post(self):
        data = request.get_json()
        if not data["comment"]:
            raise BadRequest("comment_required")
        if not data["country_name"]:
            raise BadRequest("country_name_required")
        if not data["author_id"]:
            raise BadRequest("author_id_required")
        if not (author := User.get_by_id(data["author_id"])):
            raise NotFound("entity_not_found")
        if not data["article_id"]:
            raise BadRequest("article_id_required")
        if not (article := Article.get_by_id(data["article_id"])):
            raise NotFound("entity_not_found")
        if article.max_comments <= len(article.comments):
            raise BadRequest("max_comments_reached")

        comment = Comment(
            author=author,
            article=article,
            comment=data["comment"],
            country_name=data["country_name"],
        )
        comment.save()

        return ({"comment": comment.get_full_dict()}, 201)

    def delete(self, comment_id: int):
        if not (comment := Comment.get_by_id(comment_id)):
            raise NotFound("entity_not_found")
        comment.delete()
        return "entity_deleted", 204
