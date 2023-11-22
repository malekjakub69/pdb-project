from src.resources.mysql.article import *
from src.resources.mysql.user import *
from src.resources.internal import *
from src.resources.mongo.test import *
from src.resources.mongo.user_feed import *
from src.resources.mongo.trends import *
from src.resources.mongo.users import *
from src.resources.mongo.interactions import *
from src.resources.mongo.articles import *
from src.resources.mongo.comments import *
from src.resources.mysql.test import *


def register_resources(api):
    # Internal
    api.add_resource(HealthCheckResource, "/healthcheck")
    api.add_resource(HealthCheckDatabaseResource, "/healthcheck_db")

    # MongoDB
    api.add_resource(MongoTestResource, "/mongo/test")
    api.add_resource(UserFeedResource, "/api/user_feed/<string:user_id>")
    api.add_resource(TrendsResourceWithRegion, "/api/trends/<string:timeframe>/<string:region_id>")
    api.add_resource(TrendsResourceWithoutRegion, "/api/trends/<string:timeframe>")
    api.add_resource(UsersResource, "/api/users/<string:user_id>")
    api.add_resource(LikesResource, "/api/interactions/like/<string:article_id>/<string:user_id>")
    api.add_resource(ReadsResource, "/api/interactions/read/<string:article_id>/<string:user_id>")
    api.add_resource(
        InteractionsBaseResource,
        "/api/interactions/<string:article_id>/<string:user_id>",
    )
    api.add_resource(ArticlesResource, "/api/articles/<string:article_id>")
    api.add_resource(CommentsResource, "/api/comments/<string:article_id>")

    # MySQL
    api.add_resource(MysqlTestResource, "/mysql/test")
    # USER
    api.add_resource(SQLUsersResource, "/users")  # GET all
    api.add_resource(SQLUserResource, "/user", "/user/<int:user_id>")  # GET single, POST, DELETE
    # ARTICLE
    api.add_resource(SQLArticlesResource, "/articles")  # GET all
    api.add_resource(SQLArticleResource, "/article", "/article/<int:article_id>")  # GET single, POST, DELETE
