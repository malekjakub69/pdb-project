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

### MongoDB / Read

- GET {url}/test - Tests MongoDB connection (200, OK)
- GET {url}/api/user_feed/{USER_ID} - Generates feed for user (200, OK)
- GET {url}/api/tends/{TIMEFRAME (hour | day | week | month | year)}/{?REGION_ID} - Trends per timeframe (and optionally region) (200, OK)
- GET {url}/api/users/{USER_ID} - User data (200, OK)
- GET {url}/api/interactions/{ARTICLE_ID}/{USER_ID} - If user liked and read the article (200, OK)
- - GET {url}/api/interactions/like/{ARTICLE_ID}/{USER_ID} - If user liked the article (200, OK)
- - GET {url}/api/interactions/read/{ARTICLE_ID}/{USER_ID} - If user read the article (200, OK)
- GET {url}/api/articles/{ARTICLE_ID} - Article data (200, OK)
- GET {url}/api/comments/{ARTICLE_ID} - Comments (200, OK)
  

## Data fixtures

$ python3 src/fixtures/mongo_fixtures.py