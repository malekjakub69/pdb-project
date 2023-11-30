from src.broker.wrapper import TransferObject
from src.broker.broker import get_rabbitmq_connection
import sys
import json

def comment_callback(ch, method, properties, body, mongo):
    message = body.decode()
    comments_collection = mongo.db.comments

    print('Received ' + message, file=sys.stderr, flush=True)

    try:
        data_dict = json.loads(message)
        transfer_object = TransferObject.from_dict(data_dict)

        operation = transfer_object.operation
        data = transfer_object.data

        if operation == 'insert':
            comments_collection.insert_one(data)
        elif operation == 'delete':
            comments_collection.delete_one({'_id': data['_id']})
        else:
            print(f"Unsupported operation: {operation}", file=sys.stderr, flush=True)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"Error processing message: {e}", file=sys.stderr, flush=True)

def start_comment_listener(mongo):
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    queue_name = "comment"

    channel.queue_declare(queue=queue_name)
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=lambda ch, method, properties, body: comment_callback(ch, method, properties, body, mongo),
        auto_ack=True
    )

    print('Started thread COMMENT', file=sys.stderr, flush=True)
    channel.start_consuming()
