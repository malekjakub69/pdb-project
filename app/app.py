from flask import Flask
from flask_migrate import Migrate, upgrade, init, migrate
from flask_restful import Api

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mySuperSecurePassword@db:3306/mySQLdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # create API
    api = Api(app)

    #init db

    from src.models import db, init_db

    db.init_app(app)
    init_db()

    #register resources

    from src.resources import register_resources

    register_resources(api)

    #handle migrations
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

    _ = Migrate(app, db)
    handle_migrations()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0",port=5123)