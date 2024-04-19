from flask import Blueprint, jsonify, request
from app import db
from app.models.account import Account
from app.models.non_cyclic_tile import NonCyclicTile
import uuid
from app.services.token_wrapper import need_token

non_cyclic_tile_bp = Blueprint('non_cyclic_tile_bp', __name__)

########################################################################
@non_cyclic_tile_bp.route('', methods=['POST'])
@need_token
def add_nctile(logged_account):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    
    data = request.get_json()

    tile_to_add = NonCyclicTile(
        id = data.get('id'),
        day = data.get('day'),
        meeting_id = data.get('meeting_id'),
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
@non_cyclic_tile_bp.route('/<uuid:non_cyclic_tile_id>', methods=['PUT'])
@need_token
def edit_nctile(logged_account, non_cyclic_tile_id):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    tile_to_edit = NonCyclicTile.query.filter_by(id=non_cyclic_tile_id).first()
    if tile_to_edit is None:
        return jsonify({'message': 'Tile in plan not found.'}), 404
    if not logged_account.id == tile_to_edit.account_id:
        return jsonify({"message": "Access denided, not your tile in a plan"}), 403
    
    data = request.get_json()
    tile_to_edit.day = data.get('day')
    tile_to_edit.meeting_id = data.get('meeting_id')
    tile_to_edit.allocation_id = data.get('allocation_id')

    try:
        db.session.commit()
        return jsonify({'message': 'Tile in the plan updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating tile in the plan.', 'error': str(e)}), 500
    

########################################################################
@non_cyclic_tile_bp.route('/<uuid:non_cyclic_tile_id>', methods=['DELETE'])
@need_token
def delete_nctile(logged_account, non_cyclic_tile_id):
    tile_to_delete = NonCyclicTile.query.filter_by(id=non_cyclic_tile_id).first()
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
@non_cyclic_tile_bp.route('/get_all', methods=['GET'])
@need_token
def get_all_nctiles(logged_account):
    queried_tiles = NonCyclicTile.query.filter_by(account_id=logged_account.id).all()

    tiles_to_send = []

    for tile in queried_tiles:
        til = {}
        til['id'] = tile.id
        til['day'] = tile.day
        til['meeting_id'] = tile.meeting_id
        til['allocation_id'] = tile.allocation_id
        til['schedule_id'] = tile.schedule_id
        tiles_to_send.append(til)

    return jsonify(tiles_to_send), 200