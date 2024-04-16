from flask import Blueprint, jsonify, request
from app import db
from app.models.account import Account
from app.models.schedule import Schedule
import uuid
from app.services.token_wrapper import need_token

schedule_bp = Blueprint('schedule_bp', __name__)
########################################################################
@schedule_bp.route('', methods=['POST'])
@need_token
def add_schedule(logged_account):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    
    data = request.get_json()
    
    schedule_to_add = Schedule(
        id = data.get('id'),
        schedule_name=data.get('schedule_name'),
        year=data.get('year'),
        is_cyclic=eval(data.get('is_cyclic')),
        account_id=logged_account.id
    )
    db.session.add(schedule_to_add)
    try:
        db.session.commit()
        return jsonify({'message': 'Schedule created'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating schedule.', 'error': str(e)}), 500
    
########################################################################
@schedule_bp.route('/<uuid:schedule_id>', methods=['PUT'])
@need_token
def edit_schedule(logged_account, schedule_id):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    schedule_to_edit = Schedule.query.filter_by(id=schedule_id).first()
    if schedule_to_edit is None:
        return jsonify({'message': 'Schedule not found.'}), 404
    if not logged_account.id == schedule_to_edit.account_id:
        return jsonify({"message": "Access denided, not your schedule"}), 403
    
    data = request.get_json()
    schedule_to_edit.schedule_name = data.get('schedule_name')
    schedule_to_edit.year = data.get('year')
    schedule_to_edit.is_cyclic = eval(data.get('is_cyclic'))

    try:
        db.session.commit()
        return jsonify({'message': 'Schedule updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating schedule.', 'error': str(e)}), 500
    
########################################################################
@schedule_bp.route('/<uuid:schedule_id>', methods=['DELETE'])
@need_token
def delete_schedule(logged_account, schedule_id):
    
    schedule_to_delete = Schedule.query.filter_by(id=schedule_id).first()
    if schedule_to_delete is None:
        return jsonify({'message': 'Schedule not found.'}), 404
    if not logged_account.id == schedule_to_delete.account_id:
        return jsonify({"message": "Access denided, not your schedule"}), 403
    
    db.session.delete(schedule_to_delete)

    try:
        db.session.commit()
        return jsonify({'message': 'Schedule deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting schedule.', 'error': str(e)}), 500
    


########################################################################
@schedule_bp.route('/get_all', methods=['GET'])
@need_token
def get_all_schedules(logged_account):
    queried_schedules = Schedule.query.filter_by(account_id=logged_account.id).all()

    schedules_to_send = []

    for schedule in  queried_schedules:
        sched ={}
        sched['id'] = str(schedule.id)
        sched['schedule_name'] = schedule.schedule_name
        sched['year'] = schedule.year
        sched['is_cyclic'] = schedule.is_cyclic
        schedules_to_send.append(sched)

    return jsonify(schedules_to_send), 200

    