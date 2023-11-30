folder models contains all db models 

## Endpoint list : 

### MySQL / Write

- GET {url}/healthcheck - check app healt (200, OK)
- GET {url}/healthcheck_db - check db healt (200, OK)
- GET {url}/api/mysql/users - Get all users
- GET {url}/api/mysql/user/{USER_ID} - Get a user
- POST {url}/api/mysql/user - Create a new user
- DELETE {url}/api/mysql/user/{USER_ID} - Delete a user
- GET {url}/api/mysql/articles - Get all articles
- GET {url}/api/mysql/article/{ARTICLE_ID} - Get an article
- POST {url}/api/mysql/article - Create a new article
- DELETE {url}/api/mysql/article/{ARTICLE_ID} - Delete an article
- POST {url}/api/mysql/read - Mark an article as read
- POST {url}/api/mysql/comment - Post a comment
- POST {url}/api/mysql/like - Like an article
- POST {url}/api/mysql/unlike - Unlike an article
- GET {url}/api/mysql/region/{REGION_ID} - Get region
- GET {url}/api/mysql/regions - Get all regions
- POST {url}/api/mysql/region - Create region resource
- DELETE {url}/api/mysql/region/{REGION_ID} - Delete a region

### MongoDB / Read

- GET {url}/test - Tests MongoDB connection
- GET {url}/api/user_feed/{USER_ID} - Generates feed for user
- GET {url}/api/tends/{TIMEFRAME (hour | day | week | month | year)}/{?REGION_ID} - Trends per timeframe (and optionally region)
- GET {url}/api/user/{USER_ID} - User data
- GET {url}/api/users - Users collection
- GET {url}/api/interactions/{ARTICLE_ID}/{USER_ID} - If user liked and read the article
- - GET {url}/api/interactions/like/{ARTICLE_ID}/{USER_ID} - If user liked the article
- - GET {url}/api/interactions/read/{ARTICLE_ID}/{USER_ID} - If user read the article
- GET {url}/api/article/{ARTICLE_ID} - Article data
- GET {url}/api/articles - Articles collection
- GET {url}/api/comments/{ARTICLE_ID} - Article comments
- GET {url}/api/comment/{COMMENT_ID} - Comment detail
- GET {url}/api/region/{REGION_ID} - Region detail
- GET {url}/api/regions - Region collection

## Data fixtures

$ python3 src/fixtures/mongo_fixtures.py
$ python3 src/fixtures/mysql_fixtures.py