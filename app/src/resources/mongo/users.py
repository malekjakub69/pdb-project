from flask_restful import Resource
from bson import json_util
from flask import current_app, jsonify
from bson import ObjectId


class UsersResource(Resource):
    def get(self, user_id):
        mongo = current_app.extensions["pymongo"]
        users_collection = mongo.db.users

        if not user_id.startswith("article_"):
            user_id = f"article_{user_id}"

        pipeline = [
            {"$match": {"_id": user_id}},
            {
                "$lookup": {
                    "from": "regions",
                    "localField": "region",
                    "foreignField": "_id",
                    "as": "region",
                }
            },
            {"$unwind": "$region"},
        ]

        result = users_collection.aggregate(pipeline)
        serialized_result = json_util.dumps(list(result))

        return jsonify(
            {
                "message": "User data",
                "user_id": user_id,
                "data": serialized_result,
                "data_count": len(list([result])),
            }
        )
