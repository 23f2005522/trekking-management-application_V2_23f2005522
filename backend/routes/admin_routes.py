from datetime import datetime, timedelta
import os

from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from utils.auth_utility import role_required
from utils.notification_utils import (
    email_staff_trek_assigned,
    email_staff_trek_reassigned,
    notify_staff_deactivated,
    notify_staff_reactivated,
    notify_staff_trek_assigned,
    notify_staff_trek_reassigned,
    publish_sse,
    push_sse_notifications,
)
from utils.cache_utility import clear_trekker_open_treks_cache
from model.model import *

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


# load admin dashboard stats and recent bookings/treks
@admin_bp.route("/data", methods=["GET"])
@jwt_required()
@role_required(UserRole.ADMIN)
def get_admin_data():
    if request.method == "GET":
        try:
            # fetch adminUser
            admin_user = UserModel.query.filter_by(role=UserRole.ADMIN).first()

            # fetch Dashboard stats
            total_trekkers = UserModel.query.filter_by(role=UserRole.TREKKER).count()
            total_staff = UserModel.query.filter_by(role=UserRole.STAFF).count()
            total_bookings = BookingModel.query.count()
            total_treks = TrekModel.query.count()
            total_revenue_till_data = (
                db.session.query(func.sum(BookingModel.amount_paid)).scalar() or 0
            )
            treks_approved = TrekModel.query.filter(
                TrekModel.status == TrekStatus.APPROVED
            ).count()
            treks_pending = TrekModel.query.filter(
                TrekModel.status == TrekStatus.PENDING
            ).count()

            # some recent bookings for the dashboard in JSON format
            fresh_bookings = list(
                (
                    BookingModel.query.order_by(BookingModel.booking_date.desc())
                    .limit(3)
                    .all()
                )
            )
            fresh_bookings_JSON = [
                {
                    "id": booking.id,
                    "booking_date": booking.booking_date.strftime("%d %b %Y"),
                    "booking_status": booking.status.value,
                    "amount_paid": booking.amount_paid,
                    "payment_status": booking.payment_status.value,
                    "user": {
                        "id": booking.user.id,
                        "username": booking.user.username,
                    },
                    "trek": {
                        "id": booking.trek.id,
                        "name": booking.trek.name,
                    },
                }
                for booking in fresh_bookings
            ]

            # some recent treks for the dashboard in JSON format
            fresh_treks = (
                TrekModel.query.order_by(TrekModel.created_at.desc()).limit(6).all()
            )
            fresh_treks_JSON = [
                {
                    "id": trek.id,
                    "name": trek.name,
                    "difficulty": trek.difficulty.value,
                    "location": trek.location,
                    "status": trek.status.value,
                    "assigned_staff_id": trek.staff.id if trek.staff else None,
                }
                for trek in fresh_treks
            ]

            # response data
            response = {
                "message": "Admin data fetched successfully.",
                "admin_user": {
                    "id": admin_user.id,
                    "username": admin_user.username,
                    "email": admin_user.email,
                    "phone": admin_user.phone,
                    "role": admin_user.role,
                },
                "dashboard_stats": {
                    "total_trekkers": total_trekkers,
                    "total_staff": total_staff,
                    "total_bookings": total_bookings,
                    "total_treks": total_treks,
                    "treks_approved": treks_approved,
                    "treks_pending": treks_pending,
                    "total_revenue_till_data": total_revenue_till_data,
                    "recent_bookings": fresh_bookings_JSON,
                    "recent_treks": fresh_treks_JSON,
                },
            }

            return jsonify(response), 200

        except Exception as e:
            print(f"Error fetching admin data: {str(e)}")
            response = {
                "message": "An error occurred while fetching admin data.",
            }
            return jsonify(response), 500


# trek management routes


# get all treks details
@admin_bp.route("/treks", methods=["GET"])
@jwt_required()
@role_required(UserRole.ADMIN)
def get_treks():
    try:
        treks = TrekModel.query.all()
        treks_JSON = [
            {
                "id": trek.id,
                "name": trek.name,
                "location": trek.location,
                "difficulty": trek.difficulty.value,
                "TotalSlots": trek.total_slots,
                "availableSlots": trek.available_slots,
                "status": trek.status.value,
                "assigned_staff_id": (
                    trek.assigned_staff_id if trek.assigned_staff_id else None
                ),
            }
            for trek in treks
        ]

        response = {
            "message": "Treks fetched successfully.",
            "treks": treks_JSON,
        }

        return jsonify(response), 200

    except Exception as e:
        print(f"Error fetching treks: {str(e)}")
        response = {
            "message": "An error occurred while fetching treks.",
        }
        return jsonify(response), 500


# add an new trek
@admin_bp.route("/addtrek", methods=["POST"])
@jwt_required()
@role_required(UserRole.ADMIN)
def add_trek():
    try:
        data = request.get_json(silent=True) or {}

        name = data.get("name")
        location = data.get("location")
        difficulty = data.get("difficulty")
        duration = data.get("duration")
        totalSlots = data.get("totalSlots")
        price = data.get("price")
        imageUrl = data.get("imageUrl")
        description = data.get("description")
        startDate = data.get("startDate")
        endDate = data.get("endDate")
        assignedStaffId = data.get("assignedStaffId")
       
        if assignedStaffId == "" or assignedStaffId is None:
            response = {
                "message": "Assigned staff ID is required.",
            }
            return jsonify(response), 400
            
        status = (
            TrekStatus.APPROVED
            if data.get("status") == TrekStatus.APPROVED.value
            else TrekStatus.PENDING
        )

        # same trek cant be added before the previous trek is completed
        exsiting_trek = TrekModel.query.filter_by(name=name).first()
        if exsiting_trek:
            response = {
                "message": "A trek with the same name already exists. Please wait for the previous trek to be completed before adding a new one.",
            }
            return jsonify(response), 400

        # Now this safely checks if it's an actual value or ID
        if assignedStaffId is not None:
            staff_member = StaffModel.query.filter_by(id=int(assignedStaffId)).first()
            if not staff_member:
                response = {
                    "message": "The assigned staff member does not exist.",
                }
                return jsonify(response), 400
            if staff_member.Profile_status != StaffStatus.APPROVED:
                response = {
                    "message": "Only approved staff can be assigned to treks.",
                }
                return jsonify(response), 400

        # if duration not mathcing with start and end date
        if startDate and endDate and duration:
            start_date_obj = datetime.strptime(startDate, "%Y-%m-%d")
            end_date_obj = datetime.strptime(endDate, "%Y-%m-%d")

            if end_date_obj <= start_date_obj:
                response = {
                    "message": "Ending date must be after the starting date.",
                }
                return jsonify(response), 400

            calculated_duration = (end_date_obj - start_date_obj).days + 1

            if calculated_duration != int(duration):
                response = {
                    "message": "The provided duration does not match the difference between the start and end dates.",
                }
                return jsonify(response), 400

        new_trek = TrekModel(
            name=name,
            location=location,
            difficulty=TrekDifficulty(difficulty),
            duration=int(duration),
            total_slots=int(totalSlots) if totalSlots is not None else 0,
            available_slots=int(totalSlots) if totalSlots is not None else 0,
            price=float(price),
            image_url=imageUrl,
            description=description,
            starting_at=datetime.strptime(startDate, "%Y-%m-%d"),
            ending_at=datetime.strptime(endDate, "%Y-%m-%d"),
            assigned_staff_id=int(assignedStaffId),
            status=status,
        )

        db.session.add(new_trek)

        sse_entries = []
        if staff_member:
            message = notify_staff_trek_assigned(staff_member.user_id, name)
            sse_entries.append(
                (staff_member.user_id, message, "reminder", "staff_trek_assigned")
            )

        db.session.commit()

        push_sse_notifications(sse_entries)

        if staff_member:
            email_staff_trek_assigned(staff_member.user, new_trek)

        response = {
            "message": "Trek added successfully.",
            "trek": {
                "id": new_trek.id,
                "name": new_trek.name,
                "location": new_trek.location,
                "difficulty": new_trek.difficulty.value,
                "total_slots": new_trek.total_slots,
                "available_slots": new_trek.available_slots,
                "price": new_trek.price,
                "image_url": new_trek.image_url,
                "description": new_trek.description,
                "starting_at": new_trek.starting_at.strftime("%Y-%m-%d"),
                "ending_at": new_trek.ending_at.strftime("%Y-%m-%d"),
                "assigned_staff_id": new_trek.assigned_staff_id,
            },
        }

        return jsonify(response), 201

    except IntegrityError as e:
        db.session.rollback()
        print(f"Error occurred while adding the trek: {e}")
        if "ending before start" in str(e).lower():
            message = "Ending date must be after the starting date."
        else:
            message = "Invalid trek data. Please check your inputs."
        return jsonify({"message": message}), 400

    except Exception as e:
        db.session.rollback()  # Rollback the session in case of an error
        print(f"Error occurred while adding the trek: {e}")
        response = {
            "message": "An error occurred while adding the trek.",
        }
        return jsonify(response), 500


# get trek details for edit form or save updated trek info
@admin_bp.route("/edittrek/<int:trek_id>", methods=["GET", "POST"])
@jwt_required()
@role_required(UserRole.ADMIN)
def edit_trek(trek_id):

    if request.method == "GET":
        try:
            trek = TrekModel.query.get(trek_id)
            if not trek:
                response = {
                    "message": "Trek not found.",
                }
                return jsonify(response), 404

            trek_JSON = {
                "id": trek.id,
                "name": trek.name,
                "location": trek.location,
                "difficulty": trek.difficulty.value,
                "duration": trek.duration,
                "totalSlots": trek.total_slots,
                "availableSlots": trek.available_slots,
                "price": trek.price,
                "imageUrl": trek.image_url,
                "description": trek.description,
                "startDate": trek.starting_at.strftime("%Y-%m-%d"),
                "endDate": trek.ending_at.strftime("%Y-%m-%d"),
                "assigned_staff_id": trek.assigned_staff_id,
                "status": trek.status.value,
            }

            response = {
                "message": "Trek fetched successfully.",
                "trek": trek_JSON,
            }

            return jsonify(response), 200

        except Exception as e:
            print(f"Error fetching trek: {str(e)}")
            response = {
                "message": "An error occurred while fetching the trek.",
            }
            return jsonify(response), 500

    if request.method == "POST":

        trek = TrekModel.query.filter(TrekModel.id == int(trek_id)).first()

        if not trek:
            response = {
                "message": "Trek not found.",
            }
            return jsonify(response), 404

        ## Update trek details
        try:

            data = request.get_json(silent=True)
            print(f"Received data for updating trek: {data}")

            previous_staff_id = trek.assigned_staff_id

            # check even that assigned staff exists
            assigned_staff_id = data.get("assigned_staff_id", 9999999)
            print(f"Received assigned_staff_id: {assigned_staff_id}")
            if assigned_staff_id:
                staff_member = StaffModel.query.filter_by(
                    id=int(assigned_staff_id)
                ).first()
                if not staff_member:
                    response = {
                        "message": "The assigned staff member does not exist.",
                    }
                    return jsonify(response), 400
                if staff_member.Profile_status != StaffStatus.APPROVED:
                    response = {
                        "message": "Only approved staff can be assigned to treks.",
                    }
                    return jsonify(response), 400

            trek.assigned_staff_id = (
                int(assigned_staff_id) if assigned_staff_id else None
            )

            trek.name = data.get("name", trek.name)
            trek.location = data.get("location", trek.location)
            trek.difficulty = TrekDifficulty(
                data.get("difficulty", trek.difficulty.value)
            )
            trek.duration = int(data.get("duration", trek.duration))
            trek.total_slots = int(data.get("totalSlots", trek.total_slots))
            trek.available_slots = int(data.get("availableSlots", trek.available_slots))
            trek.price = float(data.get("price", trek.price))
            trek.image_url = data.get("imageUrl", trek.image_url)
            trek.description = data.get("description", trek.description)

            start_date_str = data.get("startDate", trek.starting_at.strftime("%Y-%m-%d"))
            end_date_str = data.get("endDate", trek.ending_at.strftime("%Y-%m-%d"))
            start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d")

            if end_date_obj <= start_date_obj:
                response = {
                    "message": "Ending date must be after the starting date.",
                }
                return jsonify(response), 400

            duration_value = int(data.get("duration", trek.duration))
            calculated_duration = (end_date_obj - start_date_obj).days + 1
            if calculated_duration != duration_value:
                response = {
                    "message": "The provided duration does not match the difference between the start and end dates.",
                }
                return jsonify(response), 400

            available_slots = int(data.get("availableSlots", trek.available_slots))
            total_slots = int(data.get("totalSlots", trek.total_slots))
            if available_slots > total_slots:
                response = {
                    "message": "Available slots cannot be greater than total slots.",
                }
                return jsonify(response), 400

            trek.starting_at = start_date_obj
            trek.ending_at = end_date_obj

            status_value = data.get("status", trek.status.value)
            try:
                trek.status = TrekStatus(status_value)
            except ValueError:
                trek.status = TrekStatus.PENDING

            sse_entries = []
            new_staff_id = trek.assigned_staff_id

            if new_staff_id != previous_staff_id:
                if new_staff_id:
                    new_staff = StaffModel.query.get(new_staff_id)
                    if new_staff:
                        message = notify_staff_trek_assigned(new_staff.user_id, trek.name)
                        sse_entries.append(
                            (new_staff.user_id, message, "reminder", "staff_trek_assigned")
                        )

                if previous_staff_id and previous_staff_id != new_staff_id:
                    old_staff = StaffModel.query.get(previous_staff_id)
                    if old_staff:
                        message = notify_staff_trek_reassigned(old_staff.user_id, trek.name)
                        sse_entries.append(
                            (old_staff.user_id, message, "reminder", "staff_trek_reassigned")
                        )

            db.session.commit()
            push_sse_notifications(sse_entries)

            if new_staff_id != previous_staff_id:
                if new_staff_id:
                    assigned_staff = StaffModel.query.get(new_staff_id)
                    if assigned_staff:
                        email_staff_trek_assigned(assigned_staff.user, trek)
                if previous_staff_id and previous_staff_id != new_staff_id:
                    removed_staff = StaffModel.query.get(previous_staff_id)
                    if removed_staff:
                        email_staff_trek_reassigned(removed_staff.user, trek.name)

            response = {
                "message": "Trek updated successfully.",
                "trek": {
                    "id": trek.id,
                    "name": trek.name,
                    "location": trek.location,
                    "difficulty": trek.difficulty.value,
                    "total_slots": trek.total_slots,
                    "available_slots": trek.available_slots,
                    "price": trek.price,
                    "image_url": trek.image_url,
                    "description": trek.description,
                    "starting_at": trek.starting_at.strftime("%Y-%m-%d"),
                    "ending_at": trek.ending_at.strftime("%Y-%m-%d"),
                    "assigned_staff_id": trek.assigned_staff_id,
                    "status": trek.status.value,
                },
            }
            return jsonify(response), 200

        except IntegrityError as e:
            db.session.rollback()
            print(f"Error occurred while updating the trek: {e}")
            if "ending before start" in str(e).lower():
                message = "Ending date must be after the starting date."
            else:
                message = "Invalid trek data. Please check your inputs."
            return jsonify({"message": message}), 400

        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while updating the trek: {e}")
            response = {
                "message": "An error occurred while updating the trek.",
            }
            return jsonify(response), 500


# delete a trek when admin no longer needs it
@admin_bp.route("/deletetrek/<int:trek_id>", methods=["POST"])
@jwt_required()
@role_required(UserRole.ADMIN)
def delete_trek(trek_id):
    try:
        trek = TrekModel.query.get(trek_id)
        if not trek:
            return jsonify({"message": "Trek not found."}), 404

        trek_name = trek.name
        db.session.delete(trek)
        db.session.commit()

        return jsonify(
            {
                "message": f"Trek '{trek_name}' deleted successfully.",
                "trek_id": trek_id,
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while deleting the trek: {e}")
        return jsonify({"message": "An error occurred while deleting the trek."}), 500


# ManageStaff routes


# admin creates a new staff account (starts as pending)
@admin_bp.route("/create_staff", methods=["POST"])
@jwt_required()
@role_required(UserRole.ADMIN)
def create_staff():
    try:
        data = request.get_json(silent=True) or {}

        username = (data.get("username") or "").strip()
        email = (data.get("email") or "").strip()
        phone = (data.get("phone") or "").strip()
        password = (data.get("password") or "").strip()
        experience = data.get("experience", 0)
        address = (data.get("address") or "").strip() or None
        contact_number = (data.get("contact_number") or "").strip() or None
        staff_bio = (data.get("staff_bio") or "").strip() or None

        if not username or not email or not phone or not password:
            return jsonify({"message": "Username, email, phone, and password are required."}), 400

        if UserModel.query.filter_by(email=email).first():
            return jsonify({"message": "A user with this email already exists."}), 400

        if UserModel.query.filter_by(phone=phone).first():
            return jsonify({"message": "A user with this phone number already exists."}), 400

        user = UserModel(
            username=username,
            email=email,
            phone=phone,
            role=UserRole.STAFF.value,
            is_active=False,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        staff_profile = StaffModel(
            user_id=user.id,
            experience=int(experience) if experience is not None else 0,
            address=address,
            contact_number=contact_number,
            staff_bio=staff_bio,
            Profile_status=StaffStatus.PENDING,
        )
        db.session.add(staff_profile)
        db.session.commit()

        return jsonify(
            {
                "message": "Staff account created successfully. Approve the account before they can log in.",
                "staff": {
                    "user_id": user.id,
                    "staff_id": staff_profile.id,
                    "username": user.username,
                    "phone": user.phone,
                    "email": user.email,
                    "status": staff_profile.Profile_status.value,
                    "is_active": user.is_active,
                },
            }
        ), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while creating staff member: {e}")
        return jsonify({"message": "An error occurred while creating the staff member."}), 500


# get all staff members
@admin_bp.route("/staffs", methods=["GET"])
@jwt_required()
@role_required(UserRole.ADMIN)
def get_staffs():

    try:
        user_staff = UserModel.query.filter_by(role=UserRole.STAFF).all()

        staffs_JSON = [
            {
                "user_id": user.id,
                "staff_id": user.staff_profile.id,
                "username": user.username,
                "phone": user.phone,
                "email": user.email,
                "status": user.staff_profile.Profile_status.value,
                "is_active": user.is_active,
                "blacklisted_reason": user.blacklisted_reason,
            }
            for user in user_staff
        ]
        return jsonify({"staffs": staffs_JSON}), 200

    except Exception as e:
        print(f"Error occurred while fetching staff members: {e}")

        response = {
            "message": "An error occurred while fetching staff members.",
        }
        return jsonify(response), 500


# Approve or Reject or Blacklist or dePending staff member
@admin_bp.route("/staffs/<int:staff_id>/<string:status>", methods=["POST"])
@jwt_required()
@role_required(UserRole.ADMIN)
def update_staff_status(staff_id, status):
    try:
        staff_user = UserModel.query.filter_by(id=staff_id, role=UserRole.STAFF).first()
        if not staff_user:
            response = {
                "message": "Staff member not found.",
            }
            return jsonify(response), 404

        data = request.get_json(silent=True)
        reason = (
            data.get("reason") if data and data.get("reason") else "No reason provided"
        )

        if status.lower() == StaffStatus.APPROVED.value.lower():
            staff_user.is_blacklisted = False
            staff_user.staff_profile.Profile_status = StaffStatus.APPROVED
            staff_user.is_active = True
            staff_user.blacklisted_reason = None

        elif status.lower() == StaffStatus.REJECTED.value.lower():
            staff_user.staff_profile.Profile_status = StaffStatus.REJECTED
            staff_user.is_active = False
            staff_user.blacklisted_reason = reason

        elif status.lower() == StaffStatus.BLACKLISTED.value.lower():
            staff_user.is_blacklisted = True
            staff_user.staff_profile.Profile_status = StaffStatus.BLACKLISTED
            staff_user.is_active = False
            staff_user.blacklisted_reason = reason

        elif status.lower() == StaffStatus.PENDING.value.lower():
            staff_user.staff_profile.Profile_status = StaffStatus.PENDING
            staff_user.is_active = False
            staff_user.blacklisted_reason = None

        elif status.lower() == "deactivate":
            if staff_user.is_blacklisted:
                return jsonify({
                    "message": "Cannot deactivate a blacklisted staff member. Remove blacklist first.",
                }), 400
            if staff_user.staff_profile.Profile_status != StaffStatus.APPROVED:
                return jsonify({
                    "message": "Only approved staff can be deactivated.",
                }), 400
            staff_user.is_active = False
            staff_user.blacklisted_reason = reason
            notify_message = notify_staff_deactivated(staff_user.id, reason)

        elif status.lower() == "reactivate":
            if staff_user.is_blacklisted:
                return jsonify({
                    "message": "Cannot reactivate a blacklisted staff member. Remove blacklist first.",
                }), 400
            if staff_user.staff_profile.Profile_status != StaffStatus.APPROVED:
                return jsonify({
                    "message": "Only approved staff can be reactivated.",
                }), 400
            staff_user.is_active = True
            staff_user.blacklisted_reason = None
            notify_message = notify_staff_reactivated(staff_user.id)

        else:
            response = {
                "message": "Invalid status. Use 'approved', 'rejected', 'blacklisted', 'pending', 'deactivate', or 'reactivate'.",
            }
            return jsonify(response), 400

        db.session.commit()

        if status.lower() == "deactivate":
            publish_sse(staff_user.id, notify_message, "reminder", "staff_deactivated")
        elif status.lower() == "reactivate":
            publish_sse(staff_user.id, notify_message, "reminder", "staff_reactivated")

        response = {
            "message": f"Staff member {status} successfully.",
            "staff": {
                "user_id": staff_user.id,
                "username": staff_user.username,
                "phone": staff_user.phone,
                "email": staff_user.email,
                "status": staff_user.staff_profile.Profile_status.value,
                "is_active": staff_user.is_active,
                "blacklisted_reason": staff_user.blacklisted_reason,
            },
        }

        return jsonify(response), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while updating staff status: {e}")
        response = {
            "message": "An error occurred while updating staff status.",
        }
        return jsonify(response), 500


# Trekkers routes


# get all trekkers
@admin_bp.route("/trekkers", methods=["GET"])
@jwt_required()
@role_required(UserRole.ADMIN)
def get_trekkers():

    try:
        user_trekkers = UserModel.query.filter_by(role=UserRole.TREKKER).all()

        trekkers_JSON = [
            {
                "user_id": user.id,
                "username": user.username,
                "phone": user.phone,
                "email": user.email,
                "is_active": user.is_active,
                "is_blacklisted": user.is_blacklisted,
                "blacklisted_reason": user.blacklisted_reason,
            }
            for user in user_trekkers
        ]
        return jsonify({"trekkers": trekkers_JSON}), 200

    except Exception as e:
        print(f"Error occurred while fetching trekkers: {e}")

        response = {
            "message": "An error occurred while fetching trekkers.",
        }
        return jsonify(response), 500


# Blacklist or deBlacklist trekker
@admin_bp.route("/trekkers/<int:trekker_id>/<string:action>", methods=["POST"])
@jwt_required()
@role_required(UserRole.ADMIN)
def update_trekker_status(trekker_id, action):
    try:
        trekker_user = UserModel.query.filter_by(
            id=trekker_id, role=UserRole.TREKKER
        ).first()
        if not trekker_user:
            response = {
                "message": "Trekker not found.",
            }
            return jsonify(response), 404

        data = request.get_json(silent=True)
        reason = (
            data.get("reason") if data and data.get("reason") else "No reason provided"
        )

        if action.lower() == "blacklist":
            trekker_user.is_blacklisted = True
            trekker_user.is_active = False
            trekker_user.blacklisted_reason = reason
        elif action.lower() == "deblacklist":
            trekker_user.is_blacklisted = False
            trekker_user.is_active = True
            trekker_user.blacklisted_reason = None
        elif action.lower() == "deactivate":
            if trekker_user.is_blacklisted:
                response = {
                    "message": "Cannot deactivate a blacklisted trekker. Remove blacklist first.",
                }
                return jsonify(response), 400
            trekker_user.is_active = False
        elif action.lower() == "reactivate":
            if trekker_user.is_blacklisted:
                response = {
                    "message": "Cannot reactivate a blacklisted trekker. Remove blacklist first.",
                }
                return jsonify(response), 400
            trekker_user.is_active = True
        else:
            response = {
                "message": "Invalid action. Use 'blacklist', 'deblacklist', 'deactivate', or 'reactivate'.",
            }
            return jsonify(response), 400

        db.session.commit()

        response = {
            "message": f"Trekker {action}ed successfully.",
            "trekker": {
                "user_id": trekker_user.id,
                "username": trekker_user.username,
                "phone": trekker_user.phone,
                "email": trekker_user.email,
                "is_active": trekker_user.is_active,
                "is_blacklisted": trekker_user.is_blacklisted,
                "blacklisted_reason": trekker_user.blacklisted_reason,
            },
        }

        return jsonify(response), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while updating trekker status: {e}")
        response = {
            "message": "An error occurred while updating trekker status.",
        }
        return jsonify(response), 500


# Booking routes


# get all bookings (optional filters: search, status, payment_status, from_date, to_date)
@admin_bp.route("/bookings", methods=["GET"])
@jwt_required()
@role_required(UserRole.ADMIN)
def get_bookings():
    try:
        search = (request.args.get("search") or "").strip()
        status = (request.args.get("status") or "").strip()
        payment_status = (request.args.get("payment_status") or "").strip()
        from_date = (request.args.get("from_date") or "").strip()
        to_date = (request.args.get("to_date") or "").strip()

        query = BookingModel.query

        if status:
            query = query.filter(BookingModel.status == BookingStatus(status))

        if payment_status:
            query = query.filter(
                BookingModel.payment_status == PaymentStatus(payment_status)
            )

        if from_date:
            start = datetime.strptime(from_date, "%Y-%m-%d")
            query = query.filter(BookingModel.booking_date >= start)

        if to_date:
            end = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1)
            query = query.filter(BookingModel.booking_date < end)

        if search:
            if search.isdigit():
                query = query.filter(BookingModel.id == int(search))
            else:
                query = query.join(UserModel).join(TrekModel).filter(
                    or_(
                        UserModel.username.ilike(f"%{search}%"),
                        UserModel.email.ilike(f"%{search}%"),
                        TrekModel.name.ilike(f"%{search}%"),
                    )
                )

        bookings = query.order_by(BookingModel.booking_date.desc()).all()

        bookings_JSON = [
            {
                "id": booking.id,
                "user_id": booking.user_id,
                "username": booking.user.username,
                "user_email": booking.user.email,
                "trek_id": booking.trek_id,
                "trek_name": booking.trek.name,
                "booking_date": booking.booking_date.strftime("%Y-%m-%d"),
                "status": booking.status.value,
                "payment_status": booking.payment_status.value,
                "amount_paid": float(booking.amount_paid),
                "booking_cancel_date": (
                    booking.booking_cancel_date.strftime("%Y-%m-%d")
                    if booking.booking_cancel_date
                    else None
                ),
            }
            for booking in bookings
        ]

        return (
            jsonify(
                {
                    "message": "Bookings fetched successfully.",
                    "bookings": bookings_JSON,
                    "count": len(bookings_JSON),
                }
            ),
            200,
        )

    except ValueError as e:
        return jsonify({"message": f"Invalid filter value: {e}"}), 400
    except Exception as e:
        print(f"Error occurred while fetching bookings: {e}")
        response = {
            "message": "An error occurred while fetching bookings.",
        }
        return jsonify(response), 500


# approve trek (PENDING -> APPROVED) or open for booking (APPROVED -> OPEN)
@admin_bp.route("/treks/<int:trek_id>/status", methods=["POST"])
@jwt_required()
@role_required(UserRole.ADMIN)
def update_trek_workflow_status(trek_id):
    try:
        data = request.get_json(silent=True) or {}
        action = (data.get("action") or "").strip().lower()

        trek = TrekModel.query.get(trek_id)
        if not trek:
            return jsonify({"message": "Trek not found."}), 404

        if action == "approve":
            if trek.status != TrekStatus.PENDING:
                return jsonify(
                    {"message": "Only pending treks can be approved."}
                ), 400
            trek.status = TrekStatus.APPROVED
            message = f"Trek '{trek.name}' approved successfully."

        elif action == "open":
            if trek.status != TrekStatus.APPROVED:
                return jsonify(
                    {"message": "Only approved treks can be opened for booking."}
                ), 400
            trek.status = TrekStatus.OPEN
            clear_trekker_open_treks_cache()
            message = f"Trek '{trek.name}' is now open for booking."

        else:
            return jsonify({"message": "Invalid action. Use approve or open."}), 400

        db.session.commit()

        return jsonify(
            {
                "message": message,
                "trek": {
                    "id": trek.id,
                    "name": trek.name,
                    "status": trek.status.value,
                },
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error updating trek workflow status: {e}")
        return jsonify({"message": "An error occurred while updating trek status."}), 500


def _export_job_serializer(job):
    return {
        "id": job.id,
        "status": job.status.value if job.status else None,
        "type_of_report": job.type_of_report.value if job.type_of_report else None,
        "file_path": os.path.basename(job.file_path) if job.file_path else None,
        "created_at": job.created_at.strftime("%Y-%m-%d %H:%M:%S") if job.created_at else None,
    }


@admin_bp.route("/export-bookings", methods=["POST"])
@jwt_required()
@role_required(UserRole.ADMIN)
def start_admin_bookings_export():
    try:
        user_id = int(get_jwt_identity())
        user = UserModel.query.get(user_id)

        if not user:
            return jsonify({"message": "User not found."}), 404

        from utils.celery_health import fail_stale_export_jobs, is_celery_worker_available

        fail_stale_export_jobs(user_id=user_id)

        if not is_celery_worker_available():
            message = (
                "CSV export is unavailable right now. "
                "Please start the Celery worker and try again."
            )
            publish_sse(user.id, message, "export", action="export_failed")
            return jsonify({"message": message}), 503

        job = ExportJobModel(
            user_id=user.id,
            status=ExportStatus.PENDING,
            type_of_report=ReportType.ADMIN_BOOKINGS,
        )
        db.session.add(job)

        try:
            db.session.flush()
            from tasks import export_admin_bookings_csv

            export_admin_bookings_csv.delay(job.id)
            db.session.commit()
        except Exception as queue_error:
            db.session.rollback()
            print(f"Admin export queue failed: {queue_error}")
            message = (
                "CSV export could not be started. "
                "Ensure Redis and the Celery worker are running."
            )
            publish_sse(user.id, message, "export", action="export_failed")
            return jsonify({"message": message}), 503

        return jsonify(
            {
                "message": "Bookings export started. You will be notified when ready.",
                "job_id": job.id,
            }
        ), 202

    except Exception as e:
        db.session.rollback()
        print(f"Error starting admin export: {e}")
        return jsonify({"message": "An error occurred while starting export."}), 500


@admin_bp.route("/export-jobs", methods=["GET"])
@jwt_required()
@role_required(UserRole.ADMIN)
def list_admin_export_jobs():
    user_id = int(get_jwt_identity())

    from utils.celery_health import fail_stale_export_jobs

    fail_stale_export_jobs(user_id=user_id)

    jobs = (
        ExportJobModel.query.filter_by(user_id=user_id)
        .order_by(ExportJobModel.created_at.desc())
        .all()
    )

    return jsonify(
        {
            "message": "Export jobs fetched successfully.",
            "export_jobs": [_export_job_serializer(job) for job in jobs],
        }
    ), 200


@admin_bp.route("/export/<int:job_id>/download", methods=["GET"])
@jwt_required()
@role_required(UserRole.ADMIN)
def download_admin_export(job_id):
    user_id = int(get_jwt_identity())
    job = ExportJobModel.query.get(job_id)

    if not job or job.user_id != user_id:
        return jsonify({"message": "Export job not found."}), 404

    if job.status != ExportStatus.COMPLETED or not job.file_path:
        return jsonify({"message": "Export is not ready yet."}), 400

    if not os.path.isfile(job.file_path):
        return jsonify({"message": "Export file not found on server."}), 404

    return send_file(
        job.file_path,
        as_attachment=True,
        download_name=os.path.basename(job.file_path),
        mimetype="text/csv",
    )


# report generation routes


# pull full admin report with trek/booking/revenue breakdown
@admin_bp.route("/report", methods=["GET"])
@jwt_required()
@role_required(UserRole.ADMIN)
def generate_report():
    # Overview
    total_trekkers = UserModel.query.filter_by(role=UserRole.TREKKER).count()
    total_staff = UserModel.query.filter_by(role=UserRole.STAFF).count()
    total_treks = TrekModel.query.count()
    total_bookings = BookingModel.query.count()

    # Trek Status

    open_count = TrekModel.query.filter_by(status=TrekStatus.OPEN).count()
    ongoing_count = TrekModel.query.filter_by(status=TrekStatus.ONGOING).count()
    completed_count = TrekModel.query.filter_by(status=TrekStatus.COMPLETED).count()
    pending_count = TrekModel.query.filter_by(status=TrekStatus.PENDING).count()
    approved_count = TrekModel.query.filter_by(status=TrekStatus.APPROVED).count()

    # Booking Status

    booked = BookingModel.query.filter_by(status=BookingStatus.BOOKED).count()
    completed = BookingModel.query.filter_by(status=BookingStatus.COMPLETED).count()
    cancelled = BookingModel.query.filter_by(status=BookingStatus.CANCELED).count()

    # Payment Statistics

    paid = BookingModel.query.filter_by(payment_status=PaymentStatus.PAID).count()
    pending = BookingModel.query.filter_by(payment_status=PaymentStatus.PENDING).count()
    revenue = db.session.query(db.func.sum(BookingModel.amount_paid)).scalar() or 0

    # popular treks based on the number of bookings
    popular_treks = (
        db.session.query(
            TrekModel.name,
            db.func.count(BookingModel.id).label("booking_count"),
        )
        .join(BookingModel, BookingModel.trek_id == TrekModel.id)
        .group_by(TrekModel.id)
        .order_by(db.desc("booking_count"))
        .limit(5)
        .all()
    )

    popular_treks_JSON = [
        {"trek_name": trek.name, "booking_count": trek.booking_count}
        for trek in popular_treks
    ]

    now = datetime.utcnow()
    bookings_per_month = []
    for offset in range(5, -1, -1):
        month_index = now.month - offset
        year = now.year
        while month_index <= 0:
            month_index += 12
            year -= 1
        month_start = datetime(year, month_index, 1)
        if month_index == 12:
            month_end = datetime(year + 1, 1, 1)
        else:
            month_end = datetime(year, month_index + 1, 1)

        count = BookingModel.query.filter(
            BookingModel.booking_date >= month_start,
            BookingModel.booking_date < month_end,
        ).count()
        bookings_per_month.append({
            "label": month_start.strftime("%b %Y"),
            "count": count,
        })

    response = {
        "message": "Report generated successfully.",
        "overview": {
            "total_trekkers": total_trekkers,
            "total_staff": total_staff,
            "total_treks": total_treks,
            "total_bookings": total_bookings,
        },
        "trek_status": {
            "open": open_count,
            "ongoing": ongoing_count,
            "completed": completed_count,
            "pending": pending_count,
            "approved": approved_count,
        },
        "booking_status": {
            "booked": booked,
            "completed": completed,
            "cancelled": cancelled,
        },
        "payment_statistics": {
            "paid": paid,
            "pending": pending,
            "revenue": revenue,
        },
        "popular_treks": popular_treks_JSON,
        "charts": {
            "bookings_per_month": bookings_per_month,
            "treks_by_status": {
                "open": open_count,
                "ongoing": ongoing_count,
                "completed": completed_count,
                "pending": pending_count,
                "approved": approved_count,
            },
        },
    }

    return jsonify(response), 200
