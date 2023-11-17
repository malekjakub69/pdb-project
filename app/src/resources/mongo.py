from flask_restful import Resource
from flask_pymongo import PyMongo
from bson import json_util
from flask import current_app, jsonify

class MongoTestResource(Resource):
    def get(self):
        mongo = current_app.extensions["pymongo"]
        collection = mongo.db.articles
        documents = collection.find()

        # Serialize MongoDB documents to JSON using json_util
        serialized_documents = json_util.dumps(list(documents))

        return jsonify({
            "message": "Test Mongo endpoint",
            "documents": serialized_documents,
            "document_count": len(json_util.loads(serialized_documents)),
        })