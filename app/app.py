from flask import Flask
from flask_restful import Resource, Api

def create_app():
    app = Flask(__name__)

    api = Api(app)

    from src.resources import register_resources

    register_resources(api)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0",port=5123)