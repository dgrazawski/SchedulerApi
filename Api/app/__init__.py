from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt = JWTManager(app)

    
    from app.routes.account_routes import account_bp
    from app.routes.schedule_routes import schedule_bp
    from app.routes.lecturer_routes import lecturer_bp
    app.register_blueprint(account_bp, url_prefix='/account')
    app.register_blueprint(schedule_bp, url_prefix='/schedule')
    app.register_blueprint(lecturer_bp, url_prefix='/lecturer')
    

    return app