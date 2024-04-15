"""add test result thumbnail file id

Revision ID: a21b66c4a4fb
Revises: 980f612c0746
Create Date: 2021-11-06 17:33:06.594423

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a21b66c4a4fb"
down_revision = "980f612c0746"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("test_result_entity", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "thumbnail_file_entity_id",
                sa.Integer(),
                sa.ForeignKey("file_entity.id", name="thumbnail_file_entity_id_fk"),
                nullable=True,
            ),
        )


def downgrade():
    with op.batch_alter_table("test_result_entity") as batch_op:
        batch_op.drop_column("thumbnail_file_entity_id")
