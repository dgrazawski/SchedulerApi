from flask import Blueprint, jsonify, request
from app import db
from app.models.account import Account
from app.models.allocation import Allocation
from app.models.schedule import Schedule
from app.models.meeting import Meeting
from app.models.group import Group
from app.models.room import Room
from app.models.subject import Subject
from app.models.lecturer import Lecturer
import uuid

client_bp = Blueprint('client_bp', __name__)

@client_bp.route('/get_schedules', methods=['GET'])
def get_getschedules():
    schedules = Schedule.query.all()

    schedules_to_send = []

    for schedule in schedules:
        acc = Account.query.filter_by(id=schedule.account_id).first()
        actosend = {}
        actosend['id'] = str(schedule.id)
        actosend['schedule_name'] = schedule.schedule_name
        actosend['year'] = schedule.year
        actosend['university_name'] = acc.university_name
        actosend['faculty_name'] = acc.faculty_name
        actosend['is_cyclic'] = schedule.is_cyclic
        schedules_to_send.append(actosend)
    
    return jsonify(schedules_to_send), 200


@client_bp.route('/get_meetings/<uuid:schedule_id>', methods=['GET'])
def get_meetings_for_schedule(schedule_id):
    schedule = Schedule.query.filter_by(id=schedule_id).first()
    acc = Account.query.filter_by(id=schedule.account_id).first()
    meetings = Meeting.query.filter_by(account_id=acc.id)

    meetings_to_send = []

    for meet in meetings:
        mt = {}
        mt['id'] = str(meet.id)
        mt['start_date'] = meet.start_date
        mt['end_date'] = meet.end_date
        mt['schedule_id'] = schedule_id
        meetings_to_send.append(mt)

    return jsonify(meetings_to_send), 200

@client_bp.route('/get_allocations/<uuid:schedule_id>', methods=['GET'])
def get_allocations_for_schedule(schedule_id):
    def switch_case(argument):
        switch_dict = {
            1: "Master",
            2: "Doctor",
            3: "Habilitated Doctor",
            4: "Professor"
        }
        return switch_dict.get(argument, "Default Case")
    allocations = Allocation.query.filter_by(schedule_id=schedule_id)

    allocations_to_send = []

    for alloc in allocations:
        alts = {}
        alts['id'] = alloc.id
        alts['schedule_id'] = schedule_id
        room = Room.query.filter_by(id=alloc.room_id).first()
        alts['room_number'] = room.room_number
        group = Group.query.filter_by(id=alloc.group_id).first()
        alts['group_name'] = group.group_name
        alts['group_type'] = group.group_type
        subject = Subject.query.filter_by(id=alloc.subject_id).first()
        alts['subject_name'] = subject.subject_name
        lecturer = Lecturer.query.filter_by(id=alloc.lecturer_id).first()
        alts['lecturer_name'] = switch_case(int(lecturer.degree)) + " " + lecturer.lecturer_name + " " + lecturer.lecturer_lastname


    return jsonify(allocations_to_send), 200