from flask import Blueprint, jsonify, request
from app import db
from app.models.account import Account
from app.models.subject import Subject
import uuid
from app.services.token_wrapper import need_token

subject_bp = Blueprint('subject_bp', __name__)
########################################################################
@subject_bp.route('', methods=['POST'])
@need_token
def add_subject(logged_account):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    
    data = request.get_json()

    subject_to_add = Subject(
        id = data.get('id'),
        subject_name = data.get('subject_name'),
        year = data.get('year'),
        hours = data.get('hours'),
        lab_hours = data.get('lab_hours'),
        account_id=logged_account.id
    )

    db.session.add(subject_to_add)

    try:
        db.session.commit()
        return jsonify({'message': 'Subject created'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating subject.', 'error': str(e)}), 500
    

########################################################################
@subject_bp.route('/<uuid:subject_id>', methods=['PUT'])
@need_token
def edit_subject(logged_account, subject_id):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    subject_to_edit = Subject.query.filter_by(id=subject_id).first()
    if subject_to_edit is None:
        return jsonify({'message': 'Subject not found.'}), 404
    if not logged_account.id == subject_to_edit.account_id:
        return jsonify({"message": "Access denided, not your subject"}), 403
    
    data = request.get_json()
    subject_to_edit.subject_name = data.get('subject_name')
    subject_to_edit.year = data.get('year')
    subject_to_edit.hours = data.get('hours')
    subject_to_edit.lab_hours = data.get('lab_hours')

    try:
        db.session.commit()
        return jsonify({'message': 'Subject updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating subject.', 'error': str(e)}), 500
    

########################################################################
@subject_bp.route('/<uuid:subject_id>', methods=['DELETE'])
@need_token
def delete_subject(logged_account, subject_id):
    
    subject_to_delete = Subject.query.filter_by(id=subject_id).first()
    if subject_to_delete is None:
        return jsonify({'message': 'Subject not found.'}), 404
    if not logged_account.id == subject_to_delete.account_id:
        return jsonify({"message": "Access denided, not your subject"}), 403
    
    db.session.delete(subject_to_delete)

    try:
        db.session.commit()
        return jsonify({'message': 'Subject deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting subject.', 'error': str(e)}), 500
    

########################################################################
@subject_bp.route('/get_all', methods=['GET'])
@need_token
def get_all_subjects(logged_account):
    queried_subjects = Subject.query.filter_by(account_id=logged_account.id).all()

    subjects_to_send = []

    for subject in queried_subjects:
        sub = {}
        sub['id'] = str(subject.id)
        sub['subject_name'] = subject.subject_name
        sub['year'] = subject.year
        sub['hours'] = subject.hours
        sub['lab_hours'] = subject.lab_hours
        subjects_to_send.append(sub)

    return jsonify(subjects_to_send), 200