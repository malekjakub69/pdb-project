folder models contains all db models 

## Endpoint list : 

### MySQL / Write

- GET {url}/healthcheck - check app healt (200, OK)
- GET {url}/healthcheck_db - check db healt (200, OK) - not working yet

### MongoDB / Read

- GET {url}/test - Tests MongoDB connection (200, OK)
- GET {url}/api/user_feed/{USER_ID} - Generates feed for user (200, OK)
- GET {url}/api/tends/{TIMEFRAME (hour | day | week | month | year)}/{?REGION_ID} - Trends per timeframe (and optionally region) (200, OK)
- GET {url}/api/users/{USER_ID} - User data (200, OK)
- GET {url}/api/interactions/{ARTICLE_ID}/{USER_ID} - If user liked and read the article (200, OK)
- - GET {url}/api/interactions/like/{ARTICLE_ID}/{USER_ID} - If user liked the article (200, OK)
- - GET {url}/api/interactions/read/{ARTICLE_ID}/{USER_ID} - If user read the article (200, OK)
- GET {url}/api/articles/{ARTICLE_ID} - Article data (200, OK)

## Data fixtures

$ python3 src/fixtures/mongo_fixtures.py