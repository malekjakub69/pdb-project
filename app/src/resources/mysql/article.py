from src.models.article import Article
from flask_restful import Resource, request
from werkzeug.exceptions import NotFound, BadRequest


class SQLArticlesResource(Resource):
    def get(self):
        articles = Article.get_items()
        return ({"users": [article.get_full_dict() for article in articles]}, 200)


class SQLArticleResource(Resource):
    def get(self, article_id: int):
        if not (article := Article.get_by_id(article_id)):
            raise NotFound("entity_not_found")
        return ({"user": article.get_dict()}, 200)

    def post(self):
        data = request.get_json()

        if not data["title"]:
            raise BadRequest("title_required")

        article = Article(
            title=data["title"],
            content=data["content"],
            author_id=data["author_id"],
            perex=data["perex"],
        )
        article.save()

        return ({"user": article.get_full_dict()}, 201)

    def delete(self, article_id: int):
        if not (article := Article.get_by_id(article_id)):
            raise NotFound("entity_not_found")
        article.delete()
        return "entity_deleted", 200
