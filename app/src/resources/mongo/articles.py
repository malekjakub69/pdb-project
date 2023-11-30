from flask_restful import Resource
from bson import json_util
from flask import current_app, jsonify

class ArticleResource(Resource):
    def get(self, article_id):
        mongo = current_app.extensions["pymongo"]
        articles_collection = mongo.db.articles

        if not article_id.startswith("article_"):
            article_id = f"article_{article_id}"

        pipeline = [
            {"$match": {"_id": article_id}},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "author",
                    "foreignField": "_id",
                    "as": "author",
                }
            },
         {"$unwind": {"path": "$author", "preserveNullAndEmptyArrays": True}},
        ]

        result = articles_collection.aggregate(pipeline)
        article = list(result)
        serialized_result = json_util.dumps(article)

        return jsonify(
            {
                "message": "Article details with author",
                "article_id": article_id,
                "data": serialized_result,
                "data_count": len(article),
            }
        )
        
class ArticlesResource(Resource):
    def get(self):
        mongo = current_app.extensions["pymongo"]
        articles_collection = mongo.db.articles

        pipeline = [
            {
                "$lookup": {
                    "from": "users",
                    "localField": "author",
                    "foreignField": "_id",
                    "as": "author",
                }
           },
        {"$unwind": {"path": "$author", "preserveNullAndEmptyArrays": True}},
        ]

        all_articles = articles_collection.aggregate(pipeline)
        articles = list(all_articles)
        serialized_all_articles = json_util.dumps(articles)

        return jsonify(
            {
                "message": "All articles with authors",
                "data": serialized_all_articles,
                "data_count": len(articles),
            }
        )
