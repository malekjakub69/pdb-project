from src.broker.wrapper import TransferObject
from src.broker.broker import get_rabbitmq_connection
import sys
import json
from datetime import datetime

def like_callback(ch, method, properties, body, mongo):
    message = body.decode()
    likes_collection = mongo.db.interactions
    articles_collection = mongo.db.articles

    print('Received ' + message, file=sys.stderr, flush=True)

    try:
        data_dict = json.loads(message)
        transfer_object = TransferObject.from_dict(data_dict)

        operation = transfer_object.operation
        data = transfer_object.data

        if operation == 'insert':
            if "tags" in data and isinstance(data["tags"], str):
                data["tags"] = json.loads(data["tags"])
            if "timestamp" in data and isinstance(data["timestamp"], str):
                data["timestamp"] = datetime.strptime(data["timestamp"], "%m/%d/%Y, %H:%M:%S")
            likes_collection.insert_one(data)

            articles_collection.update_one(
                {"_id": data["article_id"]},
                {"$inc": {"like_count": 1}}
            )

        elif operation == 'delete':
            articles_collection.update_one(
                {"_id": data["article_id"]},
                {"$inc": {"like_count": -1}}
            )

            likes_collection.delete_one(data)

        else:
            print(f"Unsupported operation: {operation}", file=sys.stderr, flush=True)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"Error processing message: {e}", file=sys.stderr, flush=True)

def start_like_listener(mongo):
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    queue_name = "like"

    channel.queue_declare(queue=queue_name)
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=lambda ch, method, properties, body: like_callback(ch, method, properties, body, mongo),
        auto_ack=True
    )

    print('Started thread LIKE', file=sys.stderr, flush=True)
    channel.start_consuming()
