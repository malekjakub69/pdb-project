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
from src.resources.mongo.regions import *
from src.resources.mysql.test import *


def register_resources(api):
    # Internal
    api.add_resource(HealthCheckResource, "/healthcheck")
    api.add_resource(HealthCheckDatabaseResource, "/healthcheck_db")

    # MongoDB
    api.add_resource(MongoTestResource, "/mongo/test")
    # TRENDS
    api.add_resource(TrendsResourceWithRegion, "/api/trends/<string:timeframe>/<string:region_id>")
    api.add_resource(TrendsResourceWithoutRegion, "/api/trends/<string:timeframe>")
    # USER
    api.add_resource(UserResource, "/api/user/<string:user_id>")
    api.add_resource(UsersResource, "/api/users/")
    # FEED
    api.add_resource(UserFeedResource, "/api/user_feed/<string:user_id>")
    # INTERACTIONS
    api.add_resource(LikesResource, "/api/interactions/like/<string:article_id>/<string:user_id>")
    api.add_resource(ReadsResource, "/api/interactions/read/<string:article_id>/<string:user_id>")
    api.add_resource(
        InteractionsBaseResource,
        "/api/interactions/<string:article_id>/<string:user_id>",
    )
    # ARTICLE
    api.add_resource(ArticleResource, "/api/article/<string:article_id>")
    api.add_resource(ArticlesResource, "/api/articles")
    # COMMENT
    api.add_resource(CommentsResource, "/api/comments/<string:article_id>")
    api.add_resource(CommentResource, "/api/comment/<string:comment_id>")
    # REGION
    api.add_resource(RegionsResource, "/api/regions")
    api.add_resource(RegionResource, "/api/region/<string:region_id>")

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
