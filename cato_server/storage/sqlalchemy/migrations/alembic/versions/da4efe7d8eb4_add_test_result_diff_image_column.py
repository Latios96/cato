"""add test result diff image column

Revision ID: da4efe7d8eb4
Revises: 160df9cb588b
Create Date: 2021-07-16 14:36:21.815840

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "da4efe7d8eb4"
down_revision = "160df9cb588b"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("test_result_entity", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "diff_image_id",
                sa.Integer(),
                sa.ForeignKey("image_entity.id", name="diff_image_id_fk"),
            ),
        )


def downgrade():
    with op.batch_alter_table("test_result_entity") as batch_op:
        batch_op.drop_column("diff_image_id")
