"""remove reviews table after TrekReviewModel removal

Revision ID: 0002_remove_reviews_table
Revises: 0001_add_ongoing_trek_status
Create Date: 2026-07-10 02:20:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = "0002_remove_reviews_table"
down_revision = "0001_add_ongoing_trek_status"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    if "reviews" in inspector.get_table_names():
        op.drop_table("reviews")


def downgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    if "reviews" not in inspector.get_table_names():
        op.create_table(
            "reviews",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("trek_id", sa.Integer(), nullable=False),
            sa.Column("rating", sa.Integer(), nullable=False),
            sa.Column("comment", sa.String(length=500), nullable=True),
            sa.ForeignKeyConstraint(["trek_id"], ["treks.id"]),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
            sa.PrimaryKeyConstraint("id"),
        )
