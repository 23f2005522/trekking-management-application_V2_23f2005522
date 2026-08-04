from flask import render_template
from flask_sse import sse

from db.db import db
from model.model import NotificationModel, NotificationStatus
from utils.email_utils import send_email


def publish_sse(user_id, message, notification_type="reminder", action=None, skip_toast=False):
    payload = {"message": message, "type": notification_type}
    if action:
        payload["action"] = action
    if skip_toast:
        payload["skip_toast"] = True

    sse.publish(
        data=payload,
        type="notification",
        channel=f"user_{user_id}",
    )


def create_notification(user_id, message_text, notification_type=NotificationStatus.REMINDER):
    notification = NotificationModel(
        user_id=user_id,
        message_text=message_text,
        is_read=False,
        type_of_notification=notification_type,
        status=notification_type,
    )
    db.session.add(notification)
    return notification


def notify_staff_trek_assigned(staff_user_id, trek_name):
    message = f"You have been assigned to trek '{trek_name}'."
    create_notification(staff_user_id, message)
    return message


def notify_staff_trek_reassigned(staff_user_id, trek_name):
    message = f"Trek '{trek_name}' has been reassigned to another staff member."
    create_notification(staff_user_id, message)
    return message


def email_staff_trek_assigned(staff_user, trek):
    try:
        html_body = render_template(
            "staff_trek_assigned.html",
            staff_name=staff_user.username,
            trek_name=trek.name,
            location=trek.location,
            starting_at=trek.starting_at.strftime("%Y-%m-%d") if trek.starting_at else None,
        )
        send_email(
            staff_user.email,
            f"TrekMaster — Assigned to trek '{trek.name}'",
            html_body,
            content_type="html",
        )
    except Exception as exc:
        print(f"Staff assignment email failed for {staff_user.email}: {exc}")


def email_staff_trek_reassigned(staff_user, trek_name):
    try:
        html_body = render_template(
            "staff_trek_reassigned.html",
            staff_name=staff_user.username,
            trek_name=trek_name,
        )
        send_email(
            staff_user.email,
            f"TrekMaster — Reassigned from trek '{trek_name}'",
            html_body,
            content_type="html",
        )
    except Exception as exc:
        print(f"Staff reassignment email failed for {staff_user.email}: {exc}")


def notify_staff_deactivated(staff_user_id, reason):
    message = f"Your staff account has been deactivated. Reason: {reason}"
    create_notification(staff_user_id, message)
    return message


def notify_staff_reactivated(staff_user_id):
    message = "Your staff account has been reactivated. You can log in again."
    create_notification(staff_user_id, message)
    return message


def notify_trekker_booking(user_id, trek_name, rebook=False):
    if rebook:
        message = f"You have re-booked trek '{trek_name}' successfully."
    else:
        message = f"Your booking for trek '{trek_name}' is confirmed."
    create_notification(user_id, message, NotificationStatus.BOOKING)
    return message


def notify_trekker_booking_canceled(user_id, trek_name):
    message = f"Your booking for trek '{trek_name}' has been canceled."
    create_notification(user_id, message, NotificationStatus.BOOKING)
    return message


def push_sse_notifications(entries):
    """entries: list of (user_id, message, type_str, action_str)"""
    for entry in entries:
        user_id, message, notification_type = entry[:3]
        action = entry[3] if len(entry) > 3 else None
        publish_sse(user_id, message, notification_type, action)
