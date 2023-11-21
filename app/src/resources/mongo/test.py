from flask_restful import Resource
from flask_pymongo import PyMongo
from bson import json_util
from flask import current_app, jsonify


class MongoTestResource(Resource):
    def get(self):
        mongo = current_app.extensions["pymongo"]
        collection = mongo.db.articles
        documents = collection.find()

        serialized_documents = json_util.dumps(list(documents))

        return jsonify(
            {
                "message": "Test Mongo endpoint",
                "documents": serialized_documents,
                "document_count": documents.explain()
                .get("executionStats", {})
                .get("nReturned"),
            }
        )
