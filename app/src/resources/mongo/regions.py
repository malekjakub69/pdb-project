from flask_restful import Resource
from bson import json_util
from flask import current_app, jsonify
from bson import ObjectId


class RegionResource(Resource):
    def get(self, region_id):
        mongo = current_app.extensions["pymongo"]
        regions_collection = mongo.db.regions

        if not region_id.startswith("region_"):
            region_id = f"region_{region_id}"

        pipeline = [
            {"$match": {"_id": region_id}},
        ]

        result = regions_collection.aggregate(pipeline)
        region = list(result)

        return jsonify(
            {
                "message": "Region data",
                "region_id": region_id,
                "data": region,
                "data_count": len(region),
            }
        )

class RegionsResource(Resource):
    def get(self):
        mongo = current_app.extensions["pymongo"]
        regions_collection = mongo.db.regions

        result = regions_collection.find({})
        regions = list(result)

        return jsonify(
            {
                "message": "Regions",
                "data": regions,
                "data_count": len(regions),
            }
        )