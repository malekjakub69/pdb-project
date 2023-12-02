from flask_restful import Resource
from flask import current_app, jsonify

import sys

class UserFeedResource(Resource):
    # Gets top N tags from articles user interacts with
    def get_top_tags(self, user_id, n):
        mongo = current_app.extensions["pymongo"]
        interactions_collection = mongo.db.interactions
        if not user_id.startswith("user_"):
            user_id = f"user_{user_id}"

        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$unwind": "$tags"},
            {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": n},
            {"$project": {"_id": 1, "count": 1}},
        ]

        result = interactions_collection.aggregate(pipeline)

        serialized_result = list(result)
        return serialized_result

    # Creates feed for user
    # Articles with matching tags and not yet read
    def get_user_feed(self, user_id, user_tags):
        mongo = current_app.extensions["pymongo"]
        articles_collection = mongo.db.articles
        if not user_id.startswith("user_"):
            user_id = f"user_{user_id}"

        pipeline = [
            {
                "$lookup": {
                    "from": "interactions",
                    "let": {"articleId": "$_id", "userId": user_id},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {"$eq": ["$article_id", "$$articleId"]},
                                        {"$eq": ["$user_id", "$$userId"]},
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
        feed = list(result)
        return feed

    # User feed endpoint
    def get(self, user_id):
        top_tags = self.get_top_tags(user_id, 8)
        user_tags = [str(tag["_id"]) for tag in top_tags]
        user_feed = self.get_user_feed(user_id, user_tags)
        feed = list(user_feed)

        return jsonify(
            {
                "message": "User Feed",
                "user_id": user_id,
                "top_tags": top_tags,
                "data": feed,
                "data_count": len(user_feed)
            }
        )
