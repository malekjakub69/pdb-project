from flask_restful import Resource
from flask import current_app, jsonify


class UserResource(Resource):
    def get(self, user_id):
        mongo = current_app.extensions["pymongo"]
        users_collection = mongo.db.users

        if not user_id.startswith("user_"):
            user_id = f"user_{user_id}"

        pipeline = [
            {"$match": {"_id": user_id}},
            {
                "$lookup": {
                    "from": "regions",
                    "localField": "region_id",
                    "foreignField": "_id",
                    "as": "region_id",
                }
            },
            {"$unwind": {"path": "$region_id", "preserveNullAndEmptyArrays": True}},
        ]

        result = users_collection.aggregate(pipeline)
        user = list(result)

        return jsonify(
            {
                "message": "User data",
                "user_id": user_id,
                "data": user,
                "data_count": len(user),
            }
        )


class UsersResource(Resource):
    def get(self):
        mongo = current_app.extensions["pymongo"]
        users_collection = mongo.db.users

        pipeline = [
            {
                "$lookup": {
                    "from": "regions",
                    "localField": "region_id",
                    "foreignField": "_id",
                    "as": "region_id",
                }
            },
            {"$unwind": {"path": "$region_id", "preserveNullAndEmptyArrays": True}},
        ]

        result = users_collection.aggregate(pipeline)
        users = list(result)

        return jsonify(
            {
                "message": "Users",
                "data": users,
                "data_count": len(users),
            }
        )
