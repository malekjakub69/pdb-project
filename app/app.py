from flask import Flask
from flask_migrate import Migrate, upgrade, init, migrate
from flask_restful import Api
from flask_pymongo import PyMongo

def create_app():
    app = Flask(__name__)

    # MySQL Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mySuperSecurePassword@db:3306/mySQLdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # MongoDB Configuration
    app.config['MONGO_URI'] = 'mongodb://mongo:27017/myMongoDB'

    # Initialize MySQL
    from src.models import db, init_db
    db.init_app(app)
    init_db()

    # Initialize Flask-PyMongo
    mongo = PyMongo(app)
    # Add the PyMongo instance to the Flask app extensions
    app.extensions['pymongo'] = mongo
    
    # Register API resources
    from src.resources import register_resources
    api = Api(app)
    register_resources(api)

    # Handle MySQL migrations
    def handle_migrations():
        with app.app_context():
            try:
                # Try to create the migration repository
                init()
            except:
                # If it already exists, it's okay
                pass
            finally:
                # Always create a new migration and upgrade
                migrate(message="automatic migration")
                upgrade()

    # Initialize Flask-Migrate for MySQL
    _ = Migrate(app, db)
    handle_migrations()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5123)
