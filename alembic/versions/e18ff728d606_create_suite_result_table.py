"""create suite_result table

Revision ID: e18ff728d606
Revises: 61785bfb06f9
Create Date: 2020-11-24 17:00:23.557330

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "e18ff728d606"
down_revision = "61785bfb06f9"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "suite_result_entity",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("run_id", sa.INTEGER, sa.ForeignKey("run_entity.id")),
        sa.Column("suite_name", sa.String(), nullable=False),
        sa.Column("suite_variables", sa.JSON(), nullable=False),
    )


def downgrade():
    op.drop_table("suite_result_entity")
