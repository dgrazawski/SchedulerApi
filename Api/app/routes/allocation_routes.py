from flask import Blueprint, jsonify, request
from app import db
from app.models.account import Account
from app.models.allocation import Allocation
import uuid
from app.services.token_wrapper import need_token

allocation_bp = Blueprint('allocation_bp', __name__)

########################################################################
@allocation_bp.route('', methods=['POST'])
@need_token
def add_allocation(logged_account):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    
    data = request.get_json()

    allocation_to_add = Allocation(
        id = data.get('id'),
        lecturer_id = data.get('lecturer_id'),
        group_id = data.get('group_id'),
        subject_id = data.get('subject_id'),
        room_id = data.get('room_id'),
        schedule_id = data.get('schedule_id'),
        account_id = logged_account.id
    )

    db.session.add(allocation_to_add)

    try:
        db.session.commit()
        return jsonify({'message': 'Allocation created'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating allocation.', 'error': str(e)}), 500
    

######################################################################## 
@allocation_bp.route('/<uuid:allocation_id>', methods=['PUT'])
@need_token
def edit_allocation(logged_account, allocation_id):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    allocation_to_edit = Allocation.query.filter_by(id=allocation_id).first()
    if allocation_to_edit is None:
        return jsonify({'message': 'Group not found.'}), 404
    if not logged_account.id == allocation_to_edit.account_id:
        return jsonify({"message": "Access denided, not your group"}), 403
    
    data = request.get_json()
    allocation_to_edit.lecturer_id = data.get('lecturer_id')
    allocation_to_edit.group_id = data.get('group_id')
    allocation_to_edit.subject_id = data.get('subject_id')
    allocation_to_edit.room_id = data.get('room_id')

    try:
        db.session.commit()
        return jsonify({'message': 'Allocation updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating allocation.', 'error': str(e)}), 500
    
########################################################################
@allocation_bp.route('/<uuid:allocation_id>', methods=['DELETE'])
@need_token
def delete_allocation(logged_account, allocation_id):
    allocation_to_delete = Allocation.query.filter_by(id=allocation_id).first()
    if allocation_to_delete is None:
        return jsonify({'message': 'Allocation not found.'}), 404
    if not logged_account.id == allocation_to_delete.account_id:
        return jsonify({"message": "Access denided, not your allocation"}), 403
    
    db.session.delete(allocation_to_delete)

    try:
        db.session.commit()
        return jsonify({'message': 'Allocation deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting allocation.', 'error': str(e)}), 500
    

########################################################################
@allocation_bp.route('/get_all', methods=['GET'])
@need_token
def get_all_groups(logged_account):
    queried_allocations = Allocation.query.filter_by(account_id=logged_account.id).all()

    allocations_to_send = []

    for allocation in queried_allocations:
        alloca = {}
        alloca['id'] = allocation.id
        alloca['lecturer_id'] = allocation.lecturer_id
        alloca['group_id'] = allocation.group_id
        alloca['subject_id'] = allocation.subject_id
        alloca['room_id'] = allocation.room_id
        alloca['schedule_id'] = allocation.schedule_id
        allocations_to_send.append(alloca)

    return jsonify(allocations_to_send), 200