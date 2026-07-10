from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from utils.auth_utility import role_required
from model.model import *

staff_bp = Blueprint("staff_routes", __name__, url_prefix="/api/staff")


# small helper to turn staff user into json for frontend
def _staff_profile_json(user):
    staff_profile = user.staff_profile
    joining_date = staff_profile.joining_date

    return {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "role": "staff",
        "experience": staff_profile.experience,
        "joining_date": joining_date.strftime("%Y-%m-%d") if joining_date else None,
        "address": staff_profile.address,
        "bio": staff_profile.staff_bio,
        "profile_status": staff_profile.Profile_status.value,
    }


# load staff dashboard with assigned treks and quick stats
@staff_bp.route("/dashboard")
@jwt_required()
@role_required(UserRole.STAFF)
def dashboard():
    # get the logged-in user_Staff profile
    user_id = int(get_jwt_identity())
    user = UserModel.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    staff_profile = user.staff_profile
    assigned_treks = [treks for treks in staff_profile.treks if treks.status == TrekStatus.APPROVED  or treks.status == TrekStatus.OPEN or treks.status == TrekStatus.ONGOING or treks.status == TrekStatus.CLOSED or treks.status == TrekStatus.COMPLETED]  # from the staff_profile getting the assigned treks

    assigned_treks_list_json = []
    for trek in assigned_treks:

        total_participants = sum(
            1 for booking in trek.bookings if booking.status == BookingStatus.BOOKED
        )

        assigned_treks_list_json.append(
            {
                "id": trek.id,
                "name": trek.name,
                "location": trek.location,
                "difficulty": trek.difficulty,
                "status": trek.status.value,
                "starting_date": trek.starting_at.strftime("%Y-%m-%d"),
                "ending_date": trek.ending_at.strftime("%Y-%m-%d"),
                "total_slots": trek.total_slots,
                "available_slots": trek.available_slots,
                "total_participants": total_participants,
            }
        )

    staff_json = _staff_profile_json(user)

    return jsonify(
        {
            "message": "Welcome Staff",
            "staff_profile": staff_json,
            "assigned_treks": assigned_treks_list_json,
        }
    )


# view logged in staff profile (updates are admin only)
@staff_bp.route("/profile", methods=["GET"])
@jwt_required()
@role_required(UserRole.STAFF)
def get_staff_profile():
    user_id = int(get_jwt_identity())
    user = UserModel.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(
        {
            "message": "Staff profile fetched successfully.",
            "staff_profile": _staff_profile_json(user),
        }
    )


# Treks Related Routes

# get all treks assigned to the logged in staff member
@staff_bp.route("/treks")
@jwt_required()
@role_required(UserRole.STAFF)
def get_assigned_treks():
    user_id = int(get_jwt_identity())
    user = UserModel.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    staff_profile = user.staff_profile
    assigned_treks = [treks for treks in staff_profile.treks if treks.status == TrekStatus.APPROVED or treks.status == TrekStatus.OPEN or treks.status == TrekStatus.ONGOING or treks.status == TrekStatus.CLOSED or treks.status == TrekStatus.COMPLETED]  # from the staff_profile getting the assigned treks

    assigned_treks_list_json = []
    for trek in assigned_treks:
        total_participants = sum(
            1 for booking in trek.bookings if booking.status == BookingStatus.BOOKED
        )
        
        
        assigned_treks_list_json.append(
            {
                "id": trek.id,
                "user_staff_id": user.id,
                "assigned_staff_id": trek.assigned_staff_id,
                "name": trek.name,
                "location": trek.location,
                "difficulty": trek.difficulty,
                "status": trek.status.value,
                "starting_date": trek.starting_at.strftime("%Y-%m-%d"),
                "ending_date": trek.ending_at.strftime("%Y-%m-%d"),
                "total_slots": trek.total_slots,
                "available_slots": trek.available_slots,
                "total_participants": total_participants,
            }
        )

    # sort the assigned_treks_list_json by starting_date in ascending order
    assigned_treks_list_json.sort(key=lambda x: x["starting_date"])

    return jsonify({"assigned_treks": assigned_treks_list_json}), 200


# get one assigned trek with full details
@staff_bp.route("/treks/<int:trek_id>")
@jwt_required()
@role_required(UserRole.STAFF)
def get_assigned_trek(trek_id):
    user_id = int(get_jwt_identity())
    user = UserModel.query.get(user_id)
    trek = TrekModel.query.get(trek_id)
    print(f"User: {user}, Trek: {trek}")  # Debugging line to check values of user and trek

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not trek:
        return jsonify({"message": "Trek not found or removed"}), 404
    
    
    staff_profile = user.staff_profile # staff_profile of the logged-in user
    assigned_treks = staff_profile.treks # from the staff_profile getting the assigned treks
    
    
    # check if the trek_id is in the assigned_treks
    if trek not in assigned_treks:
        return jsonify({"message": "Trek not assigned to staff"}), 404
    
    total_participants = sum(
        1 for booking in trek.bookings if booking.status == BookingStatus.BOOKED
    )

    trek_json = {
        "id": trek.id,
        "user_staff_id": user.id,
        "assigned_staff_id": trek.assigned_staff_id,
        "name": trek.name,
        "location": trek.location,
        "difficulty": trek.difficulty.value,
        "duration": trek.duration,
        "status": trek.status.value,
        "starting_date": trek.starting_at.strftime("%Y-%m-%d"),
        "ending_date": trek.ending_at.strftime("%Y-%m-%d"),
        "total_slots": trek.total_slots,
        "available_slots": trek.available_slots,
        "total_participants": total_participants,
    }

    return jsonify({"trek": trek_json}), 200


# list all participants booked on a specific assigned trek
@staff_bp.route("/treks/<int:trek_id>/participants")
@jwt_required()
@role_required(UserRole.STAFF)
def get_trek_participants(trek_id):
    user_id = int(get_jwt_identity())
    user = UserModel.query.get(user_id)
    trek = TrekModel.query.get(trek_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not trek:
        return jsonify({"message": "Trek not found or removed"}), 404

    staff_profile = user.staff_profile
    assigned_treks = staff_profile.treks

    if trek not in assigned_treks:
        return jsonify({"message": "Trek not assigned to staff"}), 404

    participants = []
    for booking in sorted(trek.bookings, key=lambda item: item.booking_date):
        participants.append(
            {
                "id": booking.id,
                "username": booking.user.username,
                "email": booking.user.email,
                "booking_date": booking.booking_date.strftime("%d %b %Y"),
                "status": booking.status.value,
                "payment_status": booking.payment_status.value,
            }
        )

    trek_json = {
        "id": trek.id,
        "name": trek.name,
        "location": trek.location,
        "difficulty": trek.difficulty.value,
        "status": trek.status.value,
        "starting_date": trek.starting_at.strftime("%Y-%m-%d"),
        "ending_date": trek.ending_at.strftime("%Y-%m-%d"),
        "total_slots": trek.total_slots,
        "available_slots": trek.available_slots,
        "total_participants": len(participants),
    }

    return jsonify({"trek": trek_json, "participants": participants}), 200



# change trek status (open, closed, ongoing, completed etc)
@staff_bp.route("/treks/<int:trek_id>/status", methods=["POST"])
@jwt_required()
@role_required(UserRole.STAFF)
def update_assigned_trek_status(trek_id):
    user_id = int(get_jwt_identity())
    user = UserModel.query.get(user_id)
    trek = TrekModel.query.get(trek_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not trek:
        return jsonify({"message": "Trek not found or removed"}), 404

    staff_profile = user.staff_profile
    assigned_treks = staff_profile.treks

    if trek not in assigned_treks:
        return jsonify({"message": "Trek not assigned to staff"}), 404

    data = request.get_json(silent=True) or {}
    new_status = str(data.get("status", "")).lower()
    current_status = trek.status.value

    allowed_statuses = {
        TrekStatus.OPEN.value,
        TrekStatus.ONGOING.value,
        TrekStatus.CLOSED.value,
        TrekStatus.COMPLETED.value,
    }

    if new_status not in allowed_statuses:
        return (
            jsonify(
                {
                    "message": "Invalid status. Use 'open', 'ongoing', 'closed', or 'completed'."
                }
            ),
            400,
        )

    if new_status == TrekStatus.COMPLETED.value and current_status != TrekStatus.ONGOING.value:
        return (
            jsonify(
                {"message": "Trek must be marked ongoing before it can be completed."}
            ),
            400,
        )

    if new_status == TrekStatus.ONGOING.value and current_status not in (
        TrekStatus.OPEN.value,
        TrekStatus.CLOSED.value,
    ):
        return (
            jsonify(
                {"message": "Trek must be open or closed before marking ongoing."}
            ),
            400,
        )

    if new_status == TrekStatus.COMPLETED.value:
        for booking in trek.bookings:
            if booking.status == BookingStatus.BOOKED:
                booking.status = BookingStatus.COMPLETED

    try:
        trek.status = TrekStatus(new_status) # update the status of the trek to the new status as normal 
        db.session.commit()

        total_participants = sum(
            1 for booking in trek.bookings if booking.status == BookingStatus.BOOKED
        )

        trek_json = {
            "id": trek.id,
            "user_staff_id": user.id,
            "assigned_staff_id": trek.assigned_staff_id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "status": trek.status.value,
            "starting_date": trek.starting_at.strftime("%Y-%m-%d"),
            "ending_date": trek.ending_at.strftime("%Y-%m-%d"),
            "total_slots": trek.total_slots,
            "available_slots": trek.available_slots,
            "total_participants": total_participants,
        }

        return jsonify({"message": "Trek status updated successfully.", "trek": trek_json}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while updating staff trek status: {e}")
        return jsonify({"message": "An error occurred while updating trek status."}), 500


# update available slots on an assigned trek
@staff_bp.route("/treks/<int:trek_id>/slots", methods=["POST"])
@jwt_required()
@role_required(UserRole.STAFF)
def update_assigned_trek_slots(trek_id):
    user_id = int(get_jwt_identity())
    user = UserModel.query.get(user_id)
    trek = TrekModel.query.get(trek_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not trek:
        return jsonify({"message": "Trek not found or removed"}), 404

    staff_profile = user.staff_profile
    assigned_treks = staff_profile.treks

    if trek not in assigned_treks:
        return jsonify({"message": "Trek not assigned to staff"}), 404

    data = request.get_json(silent=True) or {}
    raw_available_slots = data.get("available_slots", data.get("availableSlots"))

    try:
        new_available_slots = int(raw_available_slots)
    except (TypeError, ValueError):
        return jsonify({"message": "Available slots must be a valid number."}), 400

    if new_available_slots < 0:
        return jsonify({"message": "Available slots cannot be negative."}), 400

    if new_available_slots > trek.total_slots:
        return jsonify({"message": "Available slots cannot exceed total slots."}), 400

    if new_available_slots > trek.total_slots - sum(
        1 for booking in trek.bookings if booking.status == BookingStatus.BOOKED
    ):
        return jsonify(
            {
                "message": "Available slots cannot exceed the number of unbooked slots."
            }
        ), 400

    try:
        trek.available_slots = new_available_slots
        db.session.commit()

        total_participants = sum(
            1 for booking in trek.bookings if booking.status == BookingStatus.BOOKED
        )

        trek_json = {
            "id": trek.id,
            "user_staff_id": user.id,
            "assigned_staff_id": trek.assigned_staff_id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty.value,
            "status": trek.status.value,
            "starting_date": trek.starting_at.strftime("%Y-%m-%d"),
            "ending_date": trek.ending_at.strftime("%Y-%m-%d"),
            "total_slots": trek.total_slots,
            "available_slots": trek.available_slots,
            "total_participants": total_participants,
        }

        return jsonify({"message": "Available slots updated successfully.", "trek": trek_json}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while updating trek slots: {e}")
        return jsonify({"message": "An error occurred while updating trek slots."}), 500


# toggle participant payment from pending to paid (or back)
@staff_bp.route("/treks/<int:trek_id>/participants/<int:booking_id>/payment", methods=["POST"])
@jwt_required()
@role_required(UserRole.STAFF)
def update_participant_payment_status(trek_id, booking_id):

    user_id = int(get_jwt_identity())
    user = UserModel.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    trek = TrekModel.query.get(trek_id)

    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    staff_profile = user.staff_profile

    if trek not in staff_profile.treks:
        return jsonify({"message": "This trek is not assigned to you."}), 403

    booking = BookingModel.query.filter_by(
        id=booking_id,
        trek_id=trek.id
    ).first()

    if not booking:
        return jsonify({"message": "Participant booking not found."}), 404

    try:

        if booking.payment_status == PaymentStatus.PAID:
            booking.payment_status = PaymentStatus.PENDING
            booking.amount_paid = 0

        else:
            booking.payment_status = PaymentStatus.PAID
            booking.amount_paid = trek.price

        db.session.commit()

        return jsonify({
            "message": "Payment status updated successfully.",
            "payment_status": booking.payment_status.value,
            "amount_paid": float(booking.amount_paid)
        }), 200

    except Exception as e:

        db.session.rollback()
        print(e)

        return jsonify({
            "message": "Failed to update payment status."
        }), 500





























































