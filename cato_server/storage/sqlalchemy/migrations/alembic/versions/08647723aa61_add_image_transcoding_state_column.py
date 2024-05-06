"""add_transcoding_state_column

Revision ID: 08647723aa61
Revises: b22e924ba3c2
Create Date: 2024-04-30 15:26:04.922698

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "08647723aa61"
down_revision = "b22e924ba3c2"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("image_entity", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("transcoding_state", sa.String(), nullable=True),
        )

    op.execute("update image_entity set transcoding_state='TRANSCODED'")

    with op.batch_alter_table("image_entity") as batch_op:
        batch_op.alter_column(
            "transcoding_state", existing_type=sa.String(), nullable=False
        )


def downgrade():
    with op.batch_alter_table("image_entity") as batch_op:
        batch_op.drop_column("transcoding_state")
