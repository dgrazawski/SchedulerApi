from functools import wraps
from flask import Flask, request, jsonify, make_response
from config import Config
import jwt
from app.models.account import Account
import uuid

def need_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = None
        
        if 'x-access-token' in request.headers:
            access_token = request.headers['x-access-token']

        if not access_token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 

            data = jwt.decode(access_token, Config.SECRET_KEY, ['HS256'])
            logged_id = uuid.UUID(data['id'])
            logged_account = Account.query.filter_by(id=logged_id).first()
            
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(logged_account, *args, **kwargs)
    
    return decorated