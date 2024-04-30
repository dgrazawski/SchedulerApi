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
    from app.routes.room_routes import room_bp
    from app.routes.subject_routes import subject_bp
    from app.routes.meeting_routes import meeting_bp
    from app.routes.group_routes import group_bp
    from app.routes.allocation_routes import allocation_bp
    from app.routes.cyclic_tile_route import cyclic_tile_bp
    from app.routes.non_cyclic_tile_route import non_cyclic_tile_bp
    from app.routes.client_routes import client_bp
    app.register_blueprint(account_bp, url_prefix='/account')
    app.register_blueprint(schedule_bp, url_prefix='/schedule')
    app.register_blueprint(lecturer_bp, url_prefix='/lecturer')
    app.register_blueprint(room_bp, url_prefix='/room')
    app.register_blueprint(subject_bp, url_prefix='/subject')
    app.register_blueprint(meeting_bp, url_prefix='/meeting')
    app.register_blueprint(group_bp, url_prefix='/group')
    app.register_blueprint(allocation_bp, url_prefix='/allocation')
    app.register_blueprint(cyclic_tile_bp, url_prefix='/cyclic')
    app.register_blueprint(non_cyclic_tile_bp, url_prefix='/non_cyclic')
    app.register_blueprint(client_bp, url_prefix='/client')

    return app