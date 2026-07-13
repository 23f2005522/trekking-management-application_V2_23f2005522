"""rename report_logs.file_path to report_summary

Revision ID: 0003_report_logs_report_summary
Revises: 0002_remove_reviews_table
Create Date: 2026-07-13 14:45:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "0003_report_logs_report_summary"
down_revision = "0002_remove_reviews_table"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    if "report_logs" not in inspector.get_table_names():
        return

    columns = {col["name"] for col in inspector.get_columns("report_logs")}

    if "file_path" in columns and "report_summary" not in columns:
        with op.batch_alter_table("report_logs", schema=None) as batch_op:
            batch_op.alter_column(
                "file_path",
                new_column_name="report_summary",
                existing_type=sa.String(length=200),
                type_=sa.String(length=1000),
                existing_nullable=True,
            )


def downgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    if "report_logs" not in inspector.get_table_names():
        return

    columns = {col["name"] for col in inspector.get_columns("report_logs")}

    if "report_summary" in columns and "file_path" not in columns:
        with op.batch_alter_table("report_logs", schema=None) as batch_op:
            batch_op.alter_column(
                "report_summary",
                new_column_name="file_path",
                existing_type=sa.String(length=1000),
                type_=sa.String(length=200),
                existing_nullable=True,
            )
