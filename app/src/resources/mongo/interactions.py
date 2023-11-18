from flask_restful import Resource
from bson import json_util
from flask import current_app, jsonify
from bson import ObjectId


class InteractionsBaseResource(Resource):
    def get_interactions(self, article_id, user_id, interaction_type=None):
        mongo = current_app.extensions["pymongo"]
        interactions_collection = mongo.db.interactions

        # Build the match condition based on the presence of interaction_type
        match_condition = {"article": ObjectId(article_id), "user": ObjectId(user_id)}
        if interaction_type is not None:
            match_condition["type"] = interaction_type

        pipeline = [{"$match": match_condition}]

        interactions = list(interactions_collection.aggregate(pipeline))

        serialized_result = json_util.dumps(interactions)
        return jsonify(
            {
                "message": "Article interactions",
                "user_id": user_id,
                "article_id": article_id,
                "interaction_type": interaction_type,
                "data": serialized_result,
                "data_count": len(interactions),
            }
        )

    def get(self, article_id, user_id):
        return self.get_interactions(article_id, user_id, None)


class LikesResource(InteractionsBaseResource):
    def get(self, article_id, user_id):
        return self.get_interactions(article_id, user_id, interaction_type=0)


class ReadsResource(InteractionsBaseResource):
    def get(self, article_id, user_id):
        return self.get_interactions(article_id, user_id, interaction_type=1)
