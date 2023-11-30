from faker import Faker
from pymongo import MongoClient

fake = Faker()


def generate_dummy_data():
    # Connect to MongoDB
    client = MongoClient("mongodb://mongo:27017/myMongoDB")
    db = client.myMongoDB
    articles_collection = db.articles
    users_collection = db.users
    regions_collection = db.regions
    interactions_collection = db.interactions
    comments_collection = db.comments

    print("Dropping existing collections...")
    articles_collection.drop()
    users_collection.drop()
    regions_collection.drop()
    interactions_collection.drop()
    comments_collection.drop()

    print("Creating new data...")

    regions = []
    for _ in range(5):
        region = {
            "iso_code": fake.country_code(),
            "country_name": fake.country(),
        }
        regions.append(region)
    print("Inserting regions...")
    regions_collection.insert_many(regions)

    users = []
    for _ in range(20):
        # Get a random region ID
        region_id = fake.random_element(
            elements=regions_collection.find().distinct("_id")
        )
        user = {
            "username": fake.user_name(),
            "region": region_id,
            "firstname": fake.first_name(),
            "lastname": fake.last_name(),
            "e_mail": fake.email(),
        }
        users.append(user)
    print("Inserting users...")
    users_collection.insert_many(users)

    articles = []
    for _ in range(50):
        # Get a random user GUID
        user_guid = fake.random_element(
            elements=users_collection.find().distinct("_id")
        )
        article = {
            "author": user_guid,
            "title": fake.sentence(),
            "timestamp": fake.date_time_this_decade(),
            "perex": fake.text(max_nb_chars=200),
            "content": fake.text(),
            "tags": fake.words(nb=3),
            # Like and read count are not "real" (sum (like) != article.like_count)
            "like_count": fake.random_int(0, 100),
            "read_count": fake.random_int(0, 100),
        }
        articles.append(article)
    print("Inserting articles...")
    articles_collection.insert_many(articles)

    interactions = []
    for article_id in articles_collection.find().distinct("_id"):
        liked_article = articles_collection.find_one({"_id": article_id})
        tags_from_liked_article = liked_article.get("tags", [])

        for _ in range(fake.random_int(0, 20)):
            user_id = fake.random_element(
                elements=users_collection.find().distinct("_id")
            )
            user_region = users_collection.find_one({"_id": user_id}).get("region", "")

            # 0 Like, 1 Read
            interaction = {
                "timestamp": fake.date_time_this_year(),
                "type": fake.random_element(elements=(0, 1)),
                "user_id": user_id,
                "article_id": article_id,
                "region_id": user_region,
                "tags": tags_from_liked_article,
            }
            interactions.append(interaction)
    print("Inserting interactions...")
    interactions_collection.insert_many(interactions)

    comments = []
    for article_id in articles_collection.find().distinct("_id"):
        for _ in range(fake.random_int(0, 10)):
            user_id = fake.random_element(
                elements=users_collection.find().distinct("_id")
            )

            comment = {
                "user": user_id,
                "article": article_id,
                "timestamp": fake.date_time_this_year(),
                "text": fake.text(max_nb_chars=200),
            }
            comments.append(comment)
    print("Inserting comments...")
    comments_collection.insert_many(comments)

    print("Dummy data created.")


if __name__ == "__main__":
    generate_dummy_data()
