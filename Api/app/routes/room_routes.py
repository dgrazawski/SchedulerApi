from flask import Blueprint, jsonify, request
from app import db
from app.models.account import Account
from app.models.room import Room
import uuid
from app.services.token_wrapper import need_token

room_bp = Blueprint('room_bp', __name__)

########################################################################
@room_bp.route('', methods=['POST'])
@need_token
def add_room(logged_account):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    
    data = request.get_json()

    room_to_add = Room(
        id = data.get('id'),
        room_number = data.get('room_number'),
        room_size = data.get('room_size'),
        account_id=logged_account.id
    )
    db.session.add(room_to_add)
    try:
        db.session.commit()
        return jsonify({'message': 'Room created'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating room.', 'error': str(e)}), 500
    
########################################################################
@room_bp.route('/<uuid:room_id>', methods=['PUT'])
@need_token
def edit_room(logged_account, room_id):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    room_to_edit = Room.query.filter_by(id=room_id).first()
    if room_to_edit is None:
        return jsonify({'message': 'Room not found.'}), 404
    if not logged_account.id == room_to_edit.account_id:
        return jsonify({"message": "Access denided, not your room"}), 403
    
    data = request.get_json()
    room_to_edit.room_number = data.get('room_number')
    room_to_edit.room_size = data.get('room_size')

    try:
        db.session.commit()
        return jsonify({'message': 'Room updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating room.', 'error': str(e)}), 500
    
########################################################################
@room_bp.route('/<uuid:room_id>', methods=['DELETE'])
@need_token
def delete_room(logged_account, room_id):

    room_to_delete = Room.query.filter_by(id=room_id).first()
    if room_to_delete is None:
        return jsonify({'message': 'Room not found.'}), 404
    if not logged_account.id == room_to_delete.account_id:
        return jsonify({"message": "Access denided, not your room"}), 403
    
    db.session.delete(room_to_delete)

    try:
        db.session.commit()
        return jsonify({'message': 'Room deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting room.', 'error': str(e)}), 500
    
########################################################################
@room_bp.route('/get_all', methods=['GET'])
@need_token
def get_all_rooms(logged_account):
    queried_rooms = Room.query.filter_by(account_id=logged_account.id).all()

    rooms_to_send = []

    for room in queried_rooms:
        ro = {}
        ro['id'] = str(room.id)
        ro['room_number'] = room.room_number
        ro['room_size'] = room.room_size
        rooms_to_send.append(ro)

    return jsonify(rooms_to_send), 200