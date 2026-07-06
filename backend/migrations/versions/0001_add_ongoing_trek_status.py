"""add ongoing trek status

Revision ID: 0001_add_ongoing_trek_status
Revises: 
Create Date: 2026-07-06 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_add_ongoing_trek_status"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("treks") as batch_op:
        batch_op.alter_column(
            "status",
            existing_type=sa.Enum(
                "pending",
                "approved",
                "open",
                "closed",
                "completed",
                name="trekstatus",
            ),
            type_=sa.Enum(
                "pending",
                "approved",
                "open",
                "ongoing",
                "closed",
                "completed",
                name="trekstatus",
            ),
            existing_nullable=False,
        )


def downgrade():
    with op.batch_alter_table("treks") as batch_op:
        batch_op.alter_column(
            "status",
            existing_type=sa.Enum(
                "pending",
                "approved",
                "open",
                "ongoing",
                "closed",
                "completed",
                name="trekstatus",
            ),
            type_=sa.Enum(
                "pending",
                "approved",
                "open",
                "closed",
                "completed",
                name="trekstatus",
            ),
            existing_nullable=False,
        )