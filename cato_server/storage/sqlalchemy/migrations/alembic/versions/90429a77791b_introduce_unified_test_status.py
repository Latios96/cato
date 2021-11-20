"""introduce unified test status

Revision ID: 90429a77791b
Revises: 2c8dc463a3cd
Create Date: 2021-11-13 18:04:05.006384

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import orm

# revision identifiers, used by Alembic.
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    _TestResultMapping,
)

revision = "90429a77791b"
down_revision = "2c8dc463a3cd"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("test_result_entity", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "unified_test_status",
                sa.String(),
                nullable=True,
            ),
        )

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    test_results = session.query(_TestResultMapping).all()

    for test_result in test_results:
        test_result.unified_test_status = "NOT_STARTED"
        if test_result.execution_status == "RUNNING":
            test_result.unified_test_status = "RUNNING"
        if test_result.execution_status == "FINISHED":
            if test_result.status == "FAILED":
                test_result.unified_test_status = "FAILED"
            elif test_result.status == "SUCCESS":
                test_result.unified_test_status = "SUCCESS"
    session.commit()

    with op.batch_alter_table("test_result_entity") as batch_op:
        batch_op.alter_column(
            "unified_test_status", existing_type=sa.String(), nullable=False
        )
        batch_op.alter_column(
            "execution_status", existing_type=sa.String(), nullable=True
        )


def downgrade():
    with op.batch_alter_table("test_result_entity") as batch_op:
        batch_op.drop_column("unified_test_status")
