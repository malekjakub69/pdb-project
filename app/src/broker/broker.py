import pika
import json

def get_rabbitmq_connection():
    rabbitmq_credentials = pika.PlainCredentials(
        "rabbitMqUser", "mySuperSecurePassword"
    )
    rabbitmq_parameters = pika.ConnectionParameters(
        "pdb-project_rabbitmq_1", 5672, "/", rabbitmq_credentials
    )
    return pika.BlockingConnection(rabbitmq_parameters)


def publish_to_queue(data, queue):
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    channel.queue_declare(queue=queue)
    body = json.dumps(data)
    channel.basic_publish(exchange="", routing_key=queue, body=body)

    connection.close()
