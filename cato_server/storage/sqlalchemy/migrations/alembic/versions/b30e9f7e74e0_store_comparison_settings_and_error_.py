"""store comparison settings and error value for test results

Revision ID: b30e9f7e74e0
Revises: 3e4601a725e1
Create Date: 2021-09-11 12:09:23.320378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b30e9f7e74e0"
down_revision = "3e4601a725e1"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("test_result_entity", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "comparison_settings_method",
                sa.String(),
            )
        )
        batch_op.add_column(
            sa.Column(
                "comparison_settings_threshold",
                sa.Float(),
            )
        ),
        batch_op.add_column(
            sa.Column(
                "error_value",
                sa.Float(),
            )
        )


def downgrade():
    with op.batch_alter_table("test_result_entity") as batch_op:
        batch_op.drop_column("comparison_settings_method")
        batch_op.drop_column("comparison_settings_threshold")
        batch_op.drop_column("error_value")
