from flask import Blueprint, jsonify, request
from app import db
from app.models.account import Account
from app.models.cyclic_tile import CyclicTile
import uuid
from app.services.token_wrapper import need_token

cyclic_tile_bp = Blueprint('cyclic_tile_bp', __name__)

########################################################################
@cyclic_tile_bp.route('', methods=['POST'])
@need_token
def add_ctile(logged_account):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    
    data = request.get_json()

    tile_to_add = CyclicTile(
        id = data.get('id'),
        day = data.get('day'),
        hour = data.get('hour'),
        allocation_id = data.get('allocation_id'),
        schedule_id = data.get('schedule_id'),
        account_id=logged_account.id
    )

    db.session.add(tile_to_add)

    try:
        db.session.commit()
        return jsonify({'message': 'Tile added to plan'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error adding tile to plan.', 'error': str(e)}), 500
    

########################################################################
@cyclic_tile_bp.route('/<uuid:cyclic_tile_id>', methods=['PUT'])
@need_token
def edit_ctile(logged_account, cyclic_tile_id):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    tile_to_edit = CyclicTile.query.filter_by(id=cyclic_tile_id).first()
    if tile_to_edit is None:
        return jsonify({'message': 'Tile in plan not found.'}), 404
    if not logged_account.id == tile_to_edit.account_id:
        return jsonify({"message": "Access denided, not your tile in a plan"}), 403
    
    data = request.get_json()
    tile_to_edit.day = data.get('day')
    tile_to_edit.hour = data.get('hour')
    tile_to_edit.allocation_id = data.get('allocation_id')

    try:
        db.session.commit()
        return jsonify({'message': 'Tile in the plan updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating tile in the plan.', 'error': str(e)}), 500
    

########################################################################
@cyclic_tile_bp.route('/<uuid:cyclic_tile_id>', methods=['DELETE'])
@need_token
def delete_ctile(logged_account, cyclic_tile_id):
    tile_to_delete = CyclicTile.query.filter_by(id=cyclic_tile_id).first()
    if tile_to_delete is None:
        return jsonify({'message': 'Tile in the plan not found.'}), 404
    if not logged_account.id == tile_to_delete.account_id:
        return jsonify({"message": "Access denided, not your tile in the plan"}), 403
    
    db.session.delete(tile_to_delete)

    try:
        db.session.commit()
        return jsonify({'message': 'Tile deleted from the plan'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting tile in the plan.', 'error': str(e)}), 500
    

########################################################################
@cyclic_tile_bp.route('/get_all', methods=['GET'])
@need_token
def get_all_ctiles(logged_account):
    queried_tiles = CyclicTile.query.filter_by(account_id=logged_account.id).all()

    tiles_to_send = []

    for tile in queried_tiles:
        til = {}
        til['id'] = str(tile.id)
        til['day'] = tile.day
        til['hour'] = tile.hour
        til['allocation_id'] = tile.allocation_id
        til['schedule_id'] = tile.schedule_id
        tiles_to_send.append(til)

    return jsonify(tiles_to_send), 200