from flask import Blueprint, jsonify, request
from app import db
from app.models.account import Account
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from config import Config
import uuid
from app.services.token_wrapper import need_token

account_bp = Blueprint('account_bp', __name__)

########################################################################
@account_bp.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    data = request.get_json()
    account = Account(username=data['username'], email=data['email'], university_name=data['university_name'], faculty_name=data['faculty_name'])
    account.set_password(data['password'])

    db.session.add(account)
    db.session.commit()
    return jsonify({"message": "User registered"}), 201

########################################################################
@account_bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    account = Account.query.filter_by(username=username).first()
    if not account or not check_password_hash(account.password_hashed, password):
        return jsonify({"message": "Bad username or password"}), 401

    access_token = jwt.encode({'id':str(account.id)}, Config.SECRET_KEY)
    print(access_token)
    return jsonify({'token': access_token}), 200

########################################################################
@account_bp.route('/change_pass', methods=['POST'])
@need_token
def change_password(logged_account):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    
    old_pass = request.json.get('old_pass')
    new_pass = request.json.get('new_pass')
    if not check_password_hash(logged_account.password_hashed, old_pass):
        return jsonify({"message": "Wrong password"}), 401
    
    logged_account.set_password(new_pass)
    db.session.commit()

    return jsonify({"message":"Password changed"}), 200
    