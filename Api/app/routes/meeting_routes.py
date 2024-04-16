from flask import Blueprint, jsonify, request
from app import db
from app.models.account import Account
from app.models.meeting import Meeting
import uuid
from app.services.token_wrapper import need_token

meeting_bp = Blueprint('meeting_bp', __name__)

########################################################################
@meeting_bp.route('', methods=['POST'])
@need_token
def add_meeting(logged_account):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    
    data = request.get_json()

    meeting_to_add = Meeting(
        id = data.get('id'),
        start_date = data.get('start_date'),
        end_date = data.get('end_date'),
        account_id=logged_account.id
    )
    db.session.add(meeting_to_add)

    try:
        db.session.commit()
        return jsonify({'message': 'Meeting created'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating meeting.', 'error': str(e)}), 500
    

########################################################################
@meeting_bp.route('/<uuid:meeting_id>', methods=['PUT'])
@need_token
def edit_meeting(logged_account, meeting_id):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    meeting_to_edit = Meeting.query.filter_by(id=meeting_id).first()
    if meeting_to_edit is None:
        return jsonify({'message': 'Meeting not found.'}), 404
    if not logged_account.id == meeting_to_edit.account_id:
        return jsonify({"message": "Access denided, not your meeting"}), 403
    
    data = request.get_json()
    meeting_to_edit.start_date = data.get('start_date')
    meeting_to_edit.end_date = data.get('end_date')
    
    try:
        db.session.commit()
        return jsonify({'message': 'Meeting updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating meeting.', 'error': str(e)}), 500
    

########################################################################
@meeting_bp.route('/<uuid:meeting_id>', methods=['DELETE'])
@need_token
def delete_schedule(logged_account, meeting_id):

    meeting_to_delete = Meeting.query.filter_by(id=meeting_id).first()
    if meeting_to_delete is None:
        return jsonify({'message': 'Meeting not found.'}), 404
    if not logged_account.id == meeting_to_delete.account_id:
        return jsonify({"message": "Access denided, not your meeting"}), 403
    
    db.session.delete(meeting_to_delete)

    try:
        db.session.commit()
        return jsonify({'message': 'Meeting deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting meeting.', 'error': str(e)}), 500
    

########################################################################
@meeting_bp.route('/get_all', methods=['GET'])
@need_token
def get_all_schedules(logged_account):
    queried_meetings = Meeting.query.filter_by(account_id=logged_account.id).all()

    meetings_to_send = []

    for meeting in queried_meetings:
        meet = {}
        meet['id'] = str(meeting.id)
        meet['start_date'] = meeting.start_date
        meet['end_date'] = meeting.end_date
        meetings_to_send.append(meet)

    return jsonify(meetings_to_send), 200