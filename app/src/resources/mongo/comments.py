from flask_restful import Resource
from bson import json_util
from flask import current_app, jsonify


class CommentsResource(Resource):
    def get(self, article_id):
        mongo = current_app.extensions["pymongo"]
        comments_collection = mongo.db.comments

        if not article_id.startswith("article_"):
            article_id = f"article_{article_id}"

        pipeline = [
            {"$match": {"article": article_id}},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user",
                    "foreignField": "_id",
                    "as": "user",
                }
            },
         {"$unwind": {"path": "$user", "preserveNullAndEmptyArrays": True}},
            {
                "$sort": {
                    "timestamp": -1
                }  # Sort comments by timestamp in descending order
            },
        ]

        result = comments_collection.aggregate(pipeline)
        comments = list(result)
        serialized_result = json_util.dumps(comments)

        return jsonify(
            {
                "message": "Comments for the article",
                "article_id": article_id,
                "data": serialized_result,
                "data_count": len(comments),
            }
        )

class CommentResource(Resource):
    def get(self, comment_id):
        mongo = current_app.extensions["pymongo"]
        comments_collection = mongo.db.comments

        if not comment_id.startswith("comment_"):
            comment_id = f"comment_{comment_id}"

        pipeline = [
            {"$match": {"_id": comment_id}},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user",
                    "foreignField": "_id",
                    "as": "user",
                }
            },
         {"$unwind": {"path": "$user", "preserveNullAndEmptyArrays": True}},
        ]

        result = comments_collection.aggregate(pipeline)
        comment = list(result)
        serialized_result = json_util.dumps(comment)

        return jsonify(
            {
                "message": "Comment with user detail",
                "comment_id": comment_id,
                "data": serialized_result,
                "data_count": len(comment),
            }
        )