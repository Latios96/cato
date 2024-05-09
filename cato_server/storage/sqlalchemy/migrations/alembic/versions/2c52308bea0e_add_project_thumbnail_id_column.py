"""add_project_thumbnail_id_column

Revision ID: 2c52308bea0e
Revises: 0ccfc3260d15
Create Date: 2024-05-09 17:59:29.960984

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2c52308bea0e"
down_revision = "0ccfc3260d15"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("project_entity", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "thumbnail_file_entity_id",
                sa.Integer(),
                sa.ForeignKey("file_entity.id", name="thumbnail_file_entity_id_fk"),
                nullable=True,
            ),
        )


def downgrade():
    with op.batch_alter_table("project_entity") as batch_op:
        batch_op.drop_column("thumbnail_file_entity_id")
