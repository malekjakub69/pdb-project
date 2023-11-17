from flask_restful import Resource
from bson import json_util
from flask import current_app, jsonify
from bson import ObjectId


class UserFeedResource(Resource):
    # Gets top N tags from articles user interacts with
    def get_top_tags(self, user_id, n):
        mongo = current_app.extensions["pymongo"]
        interactions_collection = mongo.db.interactions
        user_id_object = ObjectId(user_id)

        pipeline = [
            {"$match": {"user": user_id_object}},
            {"$unwind": "$tags"},
            {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": n},
            {"$project": {"_id": 1, "count": 1}},
        ]

        result = interactions_collection.aggregate(pipeline)

        serialized_result = json_util.dumps(list(result))

        return json_util.loads(serialized_result)

    # Creates feed for user
    # Articles with matching tags and not yet read
    def get_user_feed(self, user_id, user_tags):
        mongo = current_app.extensions["pymongo"]
        articles_collection = mongo.db.articles
        user_id_object = ObjectId(user_id)

        pipeline = [
            {
                "$lookup": {
                    "from": "interactions",
                    "let": {"articleId": "$_id", "userId": user_id_object},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {"$eq": ["$article", "$$articleId"]},
                                        {"$eq": ["$user", "$$userId"]},
                                        {"$eq": ["$type", 1]},  # 0 like, 1 read
                                    ]
                                }
                            }
                        }
                    ],
                    "as": "read",
                }
            },
            {
                "$match": {
                    "read": {"$eq": []},  # Filter out already read articles
                    "tags": {"$in": user_tags},  # Match articles with user's tags
                }
            },
            {
                "$addFields": {
                    "commonTags": {"$size": {"$setIntersection": ["$tags", user_tags]}}
                }
            },
            {
                "$sort": {
                    "commonTags": -1,
                    "timestamp": -1,
                }
            },
        ]

        result = articles_collection.aggregate(pipeline)

        serialized_result = json_util.dumps(list(result))

        return json_util.loads(serialized_result)

    # User feed endpoint
    def get(self, user_id):
        top_tags = self.get_top_tags(user_id, 8)
        user_tags = [str(tag["_id"]) for tag in top_tags]

        user_feed = self.get_user_feed(user_id, user_tags)

        serialized_feed = json_util.dumps(list(user_feed))

        return jsonify(
            {
                "message": "User Feed",
                "user_id": user_id,
                "top_tags": top_tags,
                "data": serialized_feed,
                "data_count": len(user_feed)
            }
        )
