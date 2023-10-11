from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

# init database
# from src.models import db, init_db

if __name__ == '__main__':
    app.run(debug=True, port=5123)