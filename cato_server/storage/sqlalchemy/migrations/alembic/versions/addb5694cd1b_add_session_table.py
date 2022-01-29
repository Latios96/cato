"""add session table

Revision ID: addb5694cd1b
Revises: 224e57808380
Create Date: 2022-01-29 18:16:12.840244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "addb5694cd1b"
down_revision = "224e57808380"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "session_entity",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("user_entity.id", name="user_id_user_entity_id_fk"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("expires_at", sa.DateTime, nullable=False),
    )


def downgrade():
    op.drop_table("session_entity")
