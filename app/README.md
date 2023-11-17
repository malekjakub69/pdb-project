folder models contains all db models 

## Endpoint list : 

### MySQL / Write

- GET {url}/healthcheck - check app healt (200, OK)
- GET {url}/healthcheck_db - check db healt (200, OK) - not working yet

### MongoDB / Read

- GET {url}/test - Tests MongoDB connection (200, OK)
- GET {url}/api/user_feed/{USER_ID} - Generates feed for user

## Data fixtures

$ python3 src/fixtures/mongo_fixtures.py