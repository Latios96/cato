"""add reference image edit value columns

Revision ID: c05d7387f7fc
Revises: 59f04b067b7f
Create Date: 2021-09-25 11:20:19.317729

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c05d7387f7fc"
down_revision = "59f04b067b7f"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("reference_image_edit_entity", schema=None) as batch_op:
        batch_op.add_column(sa.Column("old_status", sa.String, nullable=True))
        batch_op.add_column(sa.Column("new_status", sa.String, nullable=True))
        batch_op.add_column(sa.Column("old_message", sa.String, nullable=True))
        batch_op.add_column(sa.Column("new_message", sa.String, nullable=True))
        batch_op.add_column(
            sa.Column(
                "old_diff_image_id",
                sa.Integer,
                sa.ForeignKey("image_entity.id", name="old_image_output_diff_id_fk"),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "new_diff_image_id",
                sa.Integer,
                sa.ForeignKey("image_entity.id", name="new_image_output_diff_id_fk"),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "old_reference_image_id",
                sa.Integer,
                sa.ForeignKey(
                    "image_entity.id", name="old_image_output_reference_id_fk"
                ),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "new_reference_image_id",
                sa.Integer,
                sa.ForeignKey(
                    "image_entity.id", name="new_image_output_reference_id_fk"
                ),
                nullable=True,
            )
        )
        batch_op.add_column(sa.Column("old_error_value", sa.Float, nullable=True))
        batch_op.add_column(sa.Column("new_error_value", sa.Float, nullable=True))


def downgrade():
    with op.batch_alter_table("reference_image_edit_entity") as batch_op:
        batch_op.drop_column("old_status")
        batch_op.drop_column("new_status")
        batch_op.drop_column("old_message")
        batch_op.drop_column("new_message")
        batch_op.drop_column("old_diff_image_id")
        batch_op.drop_column("new_diff_image_id")
        batch_op.drop_column("old_reference_image_id")
        batch_op.drop_column("new_reference_image_id")
        batch_op.drop_column("old_error_value")
        batch_op.drop_column("new_error_value")
