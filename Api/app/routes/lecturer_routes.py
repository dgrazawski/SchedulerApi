from flask import Blueprint, jsonify, request
from app import db
from app.models.account import Account
from app.models.lecturer import Lecturer
import uuid
from app.services.token_wrapper import need_token


lecturer_bp = Blueprint('lecturer_bp', __name__)

########################################################################
@lecturer_bp.route('', methods=['POST'])
@need_token
def add_lecturer(logged_account):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    
    data = request.get_json()
    
    lecturer_to_add = Lecturer(
        id = data.get('id'),
        lecturer_name = data.get('lecturer_name'),
        lecturer_lastname = data.get('lecturer_lastname'),
        degree = data.get('degree'),
        account_id = logged_account.id
    )

    db.session.add(lecturer_to_add)
    try:
        db.session.commit()
        return jsonify({'message': 'Lecturer created'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating lecturer.', 'error': str(e)}), 500

########################################################################
@lecturer_bp.route('/<uuid:lecturer_id>', methods=['PUT'])
@need_token
def edit_lecturer(logged_account, lecturer_id):
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    lecturer_to_edit = Lecturer.query.filter_by(id=lecturer_id).first()
    if lecturer_to_edit is None:
        return jsonify({'message': 'Lecturer not found.'}), 404
    if not logged_account.id == lecturer_to_edit.account_id:
        return jsonify({"message": "Access denided, not your lecturer"}), 403
    
    data = request.get_json()
    lecturer_to_edit.lecturer_name = data.get('lecturer_name')
    lecturer_to_edit.lecturer_lastname = data.get('lecturer_lastname')
    lecturer_to_edit.degree = data.get('degree')



    try:
        db.session.commit()
        return jsonify({'message': 'Lecrurer updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating lecturer.', 'error': str(e)}), 500

########################################################################
@lecturer_bp.route('/<uuid:lecturer_id>', methods=['DELETE'])
@need_token
def delete_lecturer(logged_account, lecturer_id):
    lecturer_to_delete = Lecturer.query.filter_by(id=lecturer_id).first()
    if lecturer_to_delete is None:
        return jsonify({'message': 'Lecturer not found.'}), 404
    if not logged_account.id == lecturer_to_delete.account_id:
        return jsonify({"message": "Access denided, not your schedule"}), 403
    db.session.delete(lecturer_to_delete)

    try:
        db.session.commit()
        return jsonify({'message': 'Lecturer deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting lecturer.', 'error': str(e)}), 500

########################################################################
@lecturer_bp.route('/get_all', methods=['GET'])
@need_token
def get_all_lecturers(logged_account):
    queried_lecturers = Lecturer.query.filter_by(account_id=logged_account.id).all()

    lecturers_to_send = []

    for lecturer in queried_lecturers:
        lect = {}
        lect['id'] = str(lecturer.id)
        lect['lecturer_name'] = lecturer.lecturer_name
        lect['lecturer_lastname'] = lecturer.lecturer_lastname
        lect['degree'] = lecturer.degree
        lecturers_to_send.append(lect)

    return jsonify(lecturers_to_send), 200