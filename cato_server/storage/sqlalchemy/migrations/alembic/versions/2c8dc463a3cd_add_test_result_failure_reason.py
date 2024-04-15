"""add test result failure reason

Revision ID: 2c8dc463a3cd
Revises: a21b66c4a4fb
Create Date: 2021-11-13 10:58:23.949503

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2c8dc463a3cd"
down_revision = "a21b66c4a4fb"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("test_result_entity", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "failure_reason",
                sa.String(),
                nullable=True,
            ),
        )


def downgrade():
    with op.batch_alter_table("test_result_entity") as batch_op:
        batch_op.drop_column("failure_reason")
