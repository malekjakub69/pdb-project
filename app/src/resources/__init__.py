from src.resources.internal import *
from src.resources.mongo.test import *
from src.resources.mongo.user_feed import *
from src.resources.mongo.trends import *
from src.resources.mongo.users import *
from src.resources.mongo.interactions import *
from src.resources.mongo.articles import *


def register_resources(api):
    # Internal
    api.add_resource(HealthCheckResource, "/healthcheck")
    api.add_resource(HealthCheckDatabaseResource, "/healthcheck_db")

    # MongoDB
    api.add_resource(MongoTestResource, "/test")
    api.add_resource(UserFeedResource, "/api/user_feed/<string:user_id>")
    api.add_resource(TrendsResourceWithRegion, "/api/trends/<string:timeframe>/<string:region_id>")
    api.add_resource(TrendsResourceWithoutRegion, "/api/trends/<string:timeframe>")
    api.add_resource(UsersResource, "/api/users/<string:user_id>")
    api.add_resource(LikesResource, "/api/interactions/like/<string:article_id>/<string:user_id>")
    api.add_resource(ReadsResource, "/api/interactions/read/<string:article_id>/<string:user_id>")
    api.add_resource(InteractionsBaseResource, "/api/interactions/<string:article_id>/<string:user_id>")
    api.add_resource(ArticlesResource, "/api/articles/<string:article_id>")

