"""add celery task result tables

Revision ID: df53c5ac4840
Revises: 3984bd2a425d
Create Date: 2022-08-10 11:37:13.601604

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from celery import states
from sqlalchemy import PickleType
from sqlalchemy.schema import Sequence, CreateSequence

revision = "df53c5ac4840"
down_revision = "3984bd2a425d"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(CreateSequence(Sequence("task_id_sequence")))
    op.execute(CreateSequence(Sequence("taskset_id_sequence")))

    op.create_table(
        "celery_taskmeta",
        sa.Column(
            "id",
            sa.Integer,
            sa.Sequence("task_id_sequence"),
            primary_key=True,
            autoincrement=True,
        ),
        sa.Column("task_id", sa.String(155), unique=True),
        sa.Column("status", sa.String(50), default=states.PENDING),
        sa.Column("result", PickleType, nullable=True),
        sa.Column(
            "date_done",
            sa.DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=True,
        ),
        sa.Column("traceback", sa.Text, nullable=True),
    )

    op.create_table(
        "celery_tasksetmeta",
        sa.Column(
            "id",
            sa.Integer,
            sa.Sequence("taskset_id_sequence"),
            autoincrement=True,
            primary_key=True,
        ),
        sa.Column("taskset_id", sa.String(155), unique=True),
        sa.Column("result", PickleType, nullable=True),
        sa.Column("date_done", sa.DateTime, default=datetime.utcnow, nullable=True),
    )


def downgrade():
    op.drop_table("celery_taskmeta")
    op.drop_table("celery_tasksetmeta")
