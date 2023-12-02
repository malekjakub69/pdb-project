from flask_restful import Resource
from flask import current_app, jsonify
from datetime import timedelta, datetime

class TrendsResourceBase(Resource):
    def get_trends(self, start_date, end_date, region_id=None, limit=10):
        mongo = current_app.extensions["pymongo"]
        interactions_collection = mongo.db.interactions

        pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": start_date, "$lte": end_date},
                    # Like or read ? ...
                }
            },
            {
                "$group": {
                    "_id": "$article_id",
                    "totalInteractions": {"$sum": 1},
                }
            },
            {
                "$sort": {"totalInteractions": -1, "timestamp": -1},
            },
            {
                "$lookup": {
                    "from": "articles",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "article",
                }
            },
            {
                # Needs to be here if article not bound to the interaction (article deleted)
                "$limit": limit,
            },
            {"$unwind": "$article"},
        ]

        # Add region filter if provided
        if region_id:
            if not region_id.startswith("region_"):
                region_id = f"region_{region_id}"

            pipeline[0]["$match"]["region_id"] = region_id

        result = interactions_collection.aggregate(pipeline)

        return result


class TrendsResourceWithRegion(TrendsResourceBase):
    def get(self, timeframe, region_id):
        if timeframe == "hour":
            time_range = timedelta(hours=1)
        elif timeframe == "day":
            time_range = timedelta(days=1)
        elif timeframe == "week":
            time_range = timedelta(weeks=1)
        elif timeframe == "month":
            time_range = timedelta(days=30)
        elif timeframe == "year":
            time_range = timedelta(days=365)
        else:
            raise ValueError("Invalid timeframe")

        current_time = datetime.utcnow()
        start_date = current_time - time_range
        end_date = current_time

        trends = self.get_trends(
            start_date=start_date, end_date=end_date, region_id=region_id, limit=15
        )
        serialized_trends = list(trends)

        return jsonify(
            {
                "message": "Trends",
                "region": region_id,
                "start_date": start_date,
                "end_date": end_date,
                "timeframe": timeframe,
                "data": serialized_trends,
                "data_count": len(serialized_trends),
            }
        )


class TrendsResourceWithoutRegion(TrendsResourceBase):
    def get(self, timeframe):
        if timeframe == "hour":
            time_range = timedelta(hours=1)
        elif timeframe == "day":
            time_range = timedelta(days=1)
        elif timeframe == "week":
            time_range = timedelta(weeks=1)
        elif timeframe == "month":
            time_range = timedelta(days=30)
        elif timeframe == "year":
            time_range = timedelta(days=365)
        else:
            raise ValueError("Invalid timeframe")

        current_time = datetime.utcnow()
        start_date = current_time - time_range
        end_date = current_time

        trends = list(self.get_trends(start_date=start_date, end_date=end_date, limit=15))

        return jsonify(
            {
                "message": "Trends",
                "start_date": start_date,
                "end_date": end_date,
                "timeframe": timeframe,
                "data": trends,
                "data_count": len(trends),
            }
        )
