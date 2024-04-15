"""add_auth_user_table

Revision ID: 224e57808380
Revises: 1c7cc834809b
Create Date: 2022-01-26 19:41:55.910611

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "224e57808380"
down_revision = "1c7cc834809b"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_entity",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String, nullable=False),
        sa.Column("fullname", sa.String, nullable=False),
        sa.Column("hashed_password", sa.String, nullable=False),
    )
    op.execute("CREATE UNIQUE INDEX uq_username on user_entity (LOWER(username));")


def downgrade():
    op.drop_constraint("uq_username", "user_entity")
    op.drop_table("user_entity")
