from flask_restful import Resource
from flask import current_app, jsonify
from src.models.article import Article
import pika
import sys


class MysqlTestResource(Resource):
    def get(self):
        articles = Article.query.all()

        print('Publishing "hello" to queue "queue"', file=sys.stderr, flush=True)
        publish_to_queue("hello", "queue")

        serialized_articles = [
            {"id": article.id, "title": article.title, "content": article.content}
            for article in articles
        ]

        return jsonify(
            {
                "message": "Test MySQL endpoint",
                "articles": serialized_articles,
                "article_count": len(articles),
            }
        )


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
    channel.basic_publish(exchange="", routing_key=queue, body=data)

    connection.close()
