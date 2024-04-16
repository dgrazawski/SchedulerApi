from flask import Blueprint, jsonify, request
from app import db
from app.models.account import Account
from app.models.group import Group
import uuid
from app.services.token_wrapper import need_token

group_bp = Blueprint('group_bp', __name__)

########################################################################
@group_bp.route('', methods=['POST'])
@need_token
def add_group(logged_account):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    
    data = request.get_json()

    group_to_add = Group(
        id = data.get('id'),
        group_name = data.get('group_name'),
        group_size = data.get('group_size'),
        group_type = data.get('group_type'),
        account_id = logged_account.id,
        schedule_id = data.get('schedule_id')
    )

    db.session.add(group_to_add)

    try:
        db.session.commit()
        return jsonify({'message': 'Group created'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating group.', 'error': str(e)}), 500

######################################################################## 
@group_bp.route('/<uuid:group_id>', methods=['PUT'])
@need_token
def edit_group(logged_account, group_id):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    group_to_edit = Group.query.filter_by(id=group_id).first()
    if group_to_edit is None:
        return jsonify({'message': 'Group not found.'}), 404
    if not logged_account.id == group_to_edit.account_id:
        return jsonify({"message": "Access denided, not your group"}), 403
    
    data = request.get_json()
    group_to_edit.group_name = data.get('group_name')
    group_to_edit.group_size = data.get('group_size')
    group_to_edit.group_type = data.get('group_type')

    try:
        db.session.commit()
        return jsonify({'message': 'Group updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating group.', 'error': str(e)}), 500
    
########################################################################
@group_bp.route('/<uuid:group_id>', methods=['DELETE'])
@need_token
def delete_group(logged_account, group_id):
    group_to_delete = Group.query.filter_by(id=group_id).first()
    if group_to_delete is None:
        return jsonify({'message': 'Schedule not found.'}), 404
    if not logged_account.id == group_to_delete.account_id:
        return jsonify({"message": "Access denided, not your schedule"}), 403
    
    db.session.delete(group_to_delete)

    try:
        db.session.commit()
        return jsonify({'message': 'Group deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting group.', 'error': str(e)}), 500
    

########################################################################
@group_bp.route('/get_all', methods=['GET'])
@need_token
def get_all_groups(logged_account):
    queried_groups = Group.query.filter_by(account_id=logged_account.id).all()

    groups_to_send = []

    for group in queried_groups:
        gro = {}
        gro['id'] = str(group.id)
        gro['group_name'] = group.group_name
        gro['group_size'] = group.group_size
        gro['group_type'] = group.group_type
        gro['schedule_id'] = str(group.schedule_id)
        groups_to_send.append(gro)

    return jsonify(groups_to_send), 200