"""add image table

Revision ID: 042cc8eaf4e6
Revises: 69dfb56b8927
Create Date: 2020-12-12 11:41:55.150438

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "042cc8eaf4e6"
down_revision = "69dfb56b8927"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "image_entity",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column(
            "original_file_entity_id", sa.INTEGER, sa.ForeignKey("file_entity.id")
        ),
    )


def downgrade():
    op.drop_table("image_entity")
