from flask_restful import Resource
from bson import json_util
from flask import current_app, jsonify
from bson import ObjectId


class CommentsResource(Resource):
    def get(self, article_id):
        mongo = current_app.extensions["pymongo"]
        comments_collection = mongo.db.comments

        article_id_object = ObjectId(article_id)

        pipeline = [
            {"$match": {"article": article_id_object}},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user",
                    "foreignField": "_id",
                    "as": "user",
                }
            },
            {"$unwind": "$user"},
            {
                "$sort": {
                    "timestamp": -1
                }  # Sort comments by timestamp in descending order
            },
        ]

        result = comments_collection.aggregate(pipeline)
        serialized_result = json_util.dumps(list(result))

        return jsonify(
            {
                "message": "Comments for the article",
                "article_id": article_id,
                "data": serialized_result,
                "data_count": len(list([result])),
            }
        )
