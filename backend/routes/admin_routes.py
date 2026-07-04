from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from utils.auth_utility import role_required
from model.model import *

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


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
                    .limit(6)
                    .all()
                )
            )
            fresh_bookings_JSON = [
                {
                    "id": booking.id,
                    "booking_date": booking.booking_date.strftime("%d %b %Y"),
                    "status": booking.status.value,
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
