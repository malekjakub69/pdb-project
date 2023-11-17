from flask_restful import Resource
from bson import json_util
from flask import current_app, jsonify
from bson import ObjectId


class ArticlesResource(Resource):
    def get(self, article_id):
        mongo = current_app.extensions["pymongo"]
        articles_collection = mongo.db.articles
        users_collection = mongo.db.users

        article_id_object = ObjectId(article_id)

        pipeline = [
            {"$match": {"_id": article_id_object}},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "author",
                    "foreignField": "_id",
                    "as": "author",
                }
            },
            {"$unwind": "$author"},
        ]

        result = articles_collection.aggregate(pipeline)
        serialized_result = json_util.dumps(list(result))

        return jsonify(
            {
                "message": "Article details with author",
                "article_id": article_id,
                "data": serialized_result,
                "data_count": len(list(result)),
            }
        )
