"""add email column

Revision ID: 9bf8a029dc0e
Revises: f97c81a691c2
Create Date: 2022-03-01 14:30:13.425626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9bf8a029dc0e"
down_revision = "f97c81a691c2"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user_entity", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("email", sa.String(), nullable=True),
        )
    with op.batch_alter_table("user_entity") as batch_op:
        batch_op.alter_column("email", existing_type=sa.String(), nullable=False)
    op.execute("CREATE UNIQUE INDEX uq_email on user_entity (LOWER(email));")


def downgrade():
    with op.batch_alter_table("user_entity") as batch_op:
        batch_op.drop_column("email")
