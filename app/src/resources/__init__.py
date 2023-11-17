from src.resources.internal import *
from src.resources.mongo.test import *
from src.resources.mongo.user_feed import *


def register_resources(api):
    # Internal
    api.add_resource(HealthCheckResource, "/healthcheck")
    api.add_resource(HealthCheckDatabaseResource, "/healthcheck_db")

    # MongoDB
    api.add_resource(MongoTestResource, "/test")
    api.add_resource(UserFeedResource, "/api/user_feed/<string:user_id>")
