from flask_restful import Resource
from bson import json_util
from flask import current_app, jsonify
from bson import ObjectId

class CommentsResource(Resource):
    def get(self, article_id):
        mongo = current_app.extensions["pymongo"]

