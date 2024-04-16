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
    pass

########################################################################
@lecturer_bp.route('/<uuid:lecturer_id>', methods=['PUT'])
@need_token
def edit_lecturer(logged_account, lecturer_id):
    pass

########################################################################
@lecturer_bp.route('/<uuid:lecturer_id>', methods=['DELETE'])
@need_token
def delete_lecturer(logged_account, lecturer_id):
    pass

########################################################################
@lecturer_bp.route('/get_all', methods=['GET'])
@need_token
def get_all_lecturers(logged_account):
    pass