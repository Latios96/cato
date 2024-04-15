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

    conn = op.get_bind()
    res = conn.execute("select id, execution_status,status from test_result_entity")
    test_results = res.fetchall()

    for id, execution_status, status in test_results:
        unified_test_status = "NOT_STARTED"
        if execution_status == "RUNNING":
            unified_test_status = "RUNNING"
        if execution_status == "FINISHED":
            if status == "FAILED":
                unified_test_status = "FAILED"
            elif status == "SUCCESS":
                unified_test_status = "SUCCESS"
        test_result = (
            session.query(_TestResultMapping)
            .filter(_TestResultMapping.id == id)
            .first()
        )
        test_result.unified_test_status = unified_test_status
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
