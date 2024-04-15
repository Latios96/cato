"""add submission info table

Revision ID: b9c29616b40e
Revises: 4e83949449cb
Create Date: 2021-04-17 11:31:37.593378

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b9c29616b40e"
down_revision = "4e83949449cb"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "submission_info_entity",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("config", sa.JSON, nullable=False),
        sa.Column(
            "run_entity_id", sa.Integer, sa.ForeignKey("run_entity.id"), nullable=False
        ),
        sa.Column("resource_path", sa.String, nullable=False),
        sa.Column("executable", sa.String, nullable=False),
    )


def downgrade():
    op.drop_table("submission_info_entity")
