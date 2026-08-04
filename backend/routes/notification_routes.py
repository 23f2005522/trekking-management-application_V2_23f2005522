from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from model.model import NotificationModel, UserModel, UserRole
from db.db import db

notification_bp = Blueprint("notifications", __name__, url_prefix="/api/notifications")


def _serialize_notification(notification):
    return {
        "id": notification.id,
        "message_text": notification.message_text,
        "is_read": notification.is_read,
        "type": notification.type_of_notification.value,
        "created_at": (
            notification.created_at.strftime("%d %b %Y, %I:%M %p")
            if notification.created_at
            else None
        ),
    }


def _get_allowed_user(user_id):
    user = UserModel.query.get(user_id)
    if not user:
        return None, (jsonify({"message": "User not found."}), 404)

    if user.role not in (
        UserRole.ADMIN.value,
        UserRole.TREKKER.value,
        UserRole.STAFF.value,
    ):
        return None, (
            jsonify({"message": "Notifications are not available for this role."}),
            403,
        )

    return user, None


def _get_user_notification(notification_id, user_id):
    return NotificationModel.query.filter_by(
        id=notification_id,
        user_id=user_id,
    ).first()


@notification_bp.route("", methods=["GET"])
@jwt_required()
def get_notifications():
    user_id = int(get_jwt_identity())
    _, error_response = _get_allowed_user(user_id)
    if error_response:
        return error_response

    notifications = (
        NotificationModel.query.filter_by(user_id=user_id)
        .order_by(NotificationModel.created_at.desc())
        .all()
    )

    unread_count = NotificationModel.query.filter_by(
        user_id=user_id,
        is_read=False,
    ).count()

    return (
        jsonify(
            {
                "message": "Notifications fetched successfully.",
                "notifications": [_serialize_notification(item) for item in notifications],
                "unread_count": unread_count,
            }
        ),
        200,
    )


@notification_bp.route("/read-all", methods=["POST"])
@jwt_required()
def mark_all_notifications_read():
    user_id = int(get_jwt_identity())
    _, error_response = _get_allowed_user(user_id)
    if error_response:
        return error_response

    updated = NotificationModel.query.filter_by(
        user_id=user_id,
        is_read=False,
    ).update({"is_read": True})
    db.session.commit()

    return jsonify(
        {
            "message": "All notifications marked as read.",
            "updated_count": updated,
        }
    ), 200


@notification_bp.route("/<int:notification_id>/read", methods=["POST"])
@jwt_required()
def mark_notification_read(notification_id):
    user_id = int(get_jwt_identity())
    _, error_response = _get_allowed_user(user_id)
    if error_response:
        return error_response

    notification = _get_user_notification(notification_id, user_id)
    if not notification:
        return jsonify({"message": "Notification not found."}), 404

    if not notification.is_read:
        notification.is_read = True
        db.session.commit()

    return (
        jsonify(
            {
                "message": "Notification marked as read.",
                "notification": _serialize_notification(notification),
            }
        ),
        200,
    )


@notification_bp.route("/<int:notification_id>", methods=["DELETE"])
@jwt_required()
def delete_notification(notification_id):
    user_id = int(get_jwt_identity())
    _, error_response = _get_allowed_user(user_id)
    if error_response:
        return error_response

    notification = _get_user_notification(notification_id, user_id)
    if not notification:
        return jsonify({"message": "Notification not found."}), 404

    db.session.delete(notification)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Notification deleted successfully.",
                "notification_id": notification_id,
            }
        ),
        200,
    )
