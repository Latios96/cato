"""store test identifier for test edits

Revision ID: 980f612c0746
Revises: c05d7387f7fc
Create Date: 2021-09-26 17:10:52.454988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import orm

from cato_server.storage.sqlalchemy.sqlalchemy_test_edit_repository import (
    _TestEditMapping,
)
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    _TestResultMapping,
)

revision = "980f612c0746"
down_revision = "c05d7387f7fc"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "test_edit_entity", sa.Column("test_identifier", sa.String(), nullable=True)
    )

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    test_edits = (
        session.query(_TestEditMapping, _TestResultMapping.test_identifier)
        .join(_TestResultMapping)
        .all()
    )

    for test_edit, identifier in test_edits:
        test_edit.test_identifier = identifier
    session.commit()

    with op.batch_alter_table("test_edit_entity") as batch_op:
        batch_op.alter_column(
            "test_identifier", existing_type=sa.String(), nullable=False
        )


def downgrade():
    with op.batch_alter_table("test_edit_entity") as batch_op:
        batch_op.drop_column("test_identifier")
