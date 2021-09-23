"""add test edit schema

Revision ID: 59f04b067b7f
Revises: b30e9f7e74e0
Create Date: 2021-09-20 20:45:53.480707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "59f04b067b7f"
down_revision = "b30e9f7e74e0"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "test_edit_entity",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("test_id", sa.INTEGER, sa.ForeignKey("test_result_entity.id")),
        sa.Column("edit_type", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )
    op.create_table(
        "comparison_settings_edit_entity",
        sa.Column(
            "id", sa.INTEGER, sa.ForeignKey("test_edit_entity.id"), primary_key=True
        ),
        sa.Column("old_comparison_method", sa.String, nullable=False),
        sa.Column("new_comparison_method", sa.String, nullable=False),
        sa.Column("old_threshold", sa.FLOAT, nullable=False),
        sa.Column("new_threshold", sa.FLOAT, nullable=False),
        sa.Column("old_status", sa.String, nullable=True),
        sa.Column("new_status", sa.String, nullable=True),
        sa.Column("old_message", sa.String, nullable=True),
        sa.Column("new_message", sa.String, nullable=True),
        sa.Column(
            "old_diff_image_id",
            sa.Integer,
            sa.ForeignKey("image_entity.id"),
            nullable=True,
        ),
        sa.Column(
            "new_diff_image_id",
            sa.Integer,
            sa.ForeignKey("image_entity.id"),
            nullable=True,
        ),
        sa.Column("old_error_value", sa.Float, nullable=True),
        sa.Column("new_error_value", sa.Float, nullable=True),
    )
    op.create_table(
        "reference_image_edit_entity",
        sa.Column(
            "id", sa.INTEGER, sa.ForeignKey("test_edit_entity.id"), primary_key=True
        ),
    )


def downgrade():
    op.drop_table("test_edit_entity")
    op.drop_table("comparison_settings_edit_entity")
    op.drop_table("reference_image_edit_entity")
