from src.broker.wrapper import TransferObject
from src.broker.broker import get_rabbitmq_connection
import sys
import json

def article_callback(ch, method, properties, body, mongo):
    message = body.decode()
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

            data.pop('comments', None)
            data.pop('likes', None)
            data.pop('reads', None)
            data["like_count"] = 0
            data["read_count"] = 0
            articles_collection.insert_one(data)
        elif operation == 'delete':
            articles_collection.delete_one({'_id': data['_id']})
        else:
            print(f"Unsupported operation: {operation}", file=sys.stderr, flush=True)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"Error processing message: {e}", file=sys.stderr, flush=True)

def start_article_listener(mongo):
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    queue_name = "article"

    channel.queue_declare(queue=queue_name)
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=lambda ch, method, properties, body: article_callback(ch, method, properties, body, mongo),
        auto_ack=True
    )

    print('Started thread ARTICLE', file=sys.stderr, flush=True)
    channel.start_consuming()
