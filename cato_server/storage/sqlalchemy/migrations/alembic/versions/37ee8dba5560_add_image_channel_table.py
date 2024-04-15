"""add image channel table

Revision ID: 37ee8dba5560
Revises: 042cc8eaf4e6
Create Date: 2020-12-12 14:58:55.999562

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "37ee8dba5560"
down_revision = "042cc8eaf4e6"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "image_channel_entity",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("image_entity_id", sa.INTEGER, sa.ForeignKey("image_entity.id")),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("file_entity_id", sa.INTEGER, sa.ForeignKey("file_entity.id")),
    )


def downgrade():
    op.drop_table("image_channel_entity")
