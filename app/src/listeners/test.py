from src.resources.mysql.test import get_rabbitmq_connection
import sys

def test_callback(ch, method, properties, body, mongo):
    message = body.decode()

    db = mongo.db

    print('Received '+message, file=sys.stderr, flush=True)
    
def start_test_listener(mongo):
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    queue_name = "queue"

    channel.queue_declare(queue=queue_name)
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=lambda ch, method, properties, body: test_callback(ch, method, properties, body, mongo),
        auto_ack=True
    )

    print('Started thread TEST', file=sys.stderr, flush=True)
    channel.start_consuming()
