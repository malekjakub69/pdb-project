from src.resources.mysql.comment import *
from src.resources.mysql.like import *
from src.resources.mysql.read import *
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
    api.add_resource(UserFeedResource, "/api/user_feed/<int:user_id>")
    api.add_resource(TrendsResourceWithRegion, "/api/trends/<int:timeframe>/<int:region_id>")
    api.add_resource(TrendsResourceWithoutRegion, "/api/trends/<int:timeframe>")
    api.add_resource(UsersResource, "/api/users/<int:user_id>")
    api.add_resource(LikesResource, "/api/interactions/like/<int:article_id>/<int:user_id>")
    api.add_resource(ReadsResource, "/api/interactions/read/<int:article_id>/<int:user_id>")
    api.add_resource(
        InteractionsBaseResource,
        "/api/interactions/<int:article_id>/<int:user_id>",
    )
    api.add_resource(ArticlesResource, "/api/articles/<int:article_id>")
    api.add_resource(CommentsResource, "/api/comments/<int:article_id>")

    # MySQL
    api.add_resource(MysqlTestResource, "/api/mysql/test")
    # USER
    api.add_resource(SQLUsersResource, "/api/mysql/users")  # GET all
    api.add_resource(SQLUserResource, "/api/mysql/user", "/api/mysql/user/<int:user_id>")  # GET single, POST, DELETE
    # ARTICLE
    api.add_resource(SQLArticlesResource, "/api/mysql/articles")  # GET all
    api.add_resource(
        SQLArticleResource, "/api/mysql/article", "/api/mysql/article/<int:article_id>"
    )  # GET single, POST, DELETE
    # READ
    api.add_resource(SQLReadResource, "/api/mysql/read")  # POST
    # COMMENT
    api.add_resource(SQLCommentResource, "/api/mysql/comment")  # POST
    # LIKE
    api.add_resource(SQLLikeResource, "/api/mysql/like")  # POST
    api.add_resource(SQLUnlikeResource, "/api/mysql/unlike")  # POST
