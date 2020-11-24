"""create test_result table

Revision ID: 20aef8e365cf
Revises: e18ff728d606
Create Date: 2020-11-24 17:30:07.421161

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20aef8e365cf"
down_revision = "e18ff728d606"
branch_labels = None
depends_on = None
op.create_table(
    "test_result_entity",
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column(
        "suite_result_entity_id", sa.Integer, sa.ForeignKey("suite_result_entity.id")
    ),
    sa.Column("test_name", sa.String(), nullable=False),
    sa.Column("test_command", sa.String(), nullable=False),
    sa.Column("test_variables", sa.JSON(), nullable=False),
    sa.Column("execution_status", sa.String(), nullable=False),
    sa.Column("status", sa.String(), nullable=True),
    sa.Column("output", sa.JSON(), nullable=True),
    sa.Column("seconds", sa.FLOAT(), nullable=True),
    sa.Column("message", sa.String(), nullable=True),
    sa.Column("image_output", sa.String(), nullable=True),
    sa.Column("reference_image", sa.String(), nullable=True),
    sa.Column("started_at", sa.DateTime, nullable=True),
    sa.Column("finished_at", sa.DateTime, nullable=True),
)


def upgrade():
    pass


def downgrade():
    op.drop_table("test_result_entity")
