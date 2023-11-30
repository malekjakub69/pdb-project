from src.broker.wrapper import TransferObject
from src.broker.broker import get_rabbitmq_connection
import sys
import json

def read_callback(ch, method, properties, body, mongo):
    message = body.decode()
    reads_collection = mongo.db.interactions
    articles_collection = mongo.db.articles
    users_collection = mongo.db.users

    print('Received ' + message, file=sys.stderr, flush=True)

    try:
        data_dict = json.loads(message)
        transfer_object = TransferObject.from_dict(data_dict)

        operation = transfer_object.operation
        data = transfer_object.data

        if operation == 'insert':
            reads_collection.insert_one(data)

            articles_collection.update_one(
                {"_id": data["article_id"]},
                {"$inc": {"read_count": 1}}
            )
        else:
            print(f"Unsupported operation: {operation}", file=sys.stderr, flush=True)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"Error processing message: {e}", file=sys.stderr, flush=True)

def start_read_listener(mongo):
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    queue_name = "read"

    channel.queue_declare(queue=queue_name)
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=lambda ch, method, properties, body: read_callback(ch, method, properties, body, mongo),
        auto_ack=True
    )

    print('Started thread READ', file=sys.stderr, flush=True)
    channel.start_consuming()