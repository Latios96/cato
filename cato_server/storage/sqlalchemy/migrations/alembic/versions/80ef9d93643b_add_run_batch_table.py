"""add run batch table

Revision ID: 80ef9d93643b
Revises: df53c5ac4840
Create Date: 2022-09-15 16:11:51.003017

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "80ef9d93643b"
down_revision = "df53c5ac4840"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "run_batch_entity",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("provider", sa.String, nullable=False),
        sa.Column("run_name", sa.String, nullable=False),
        sa.Column("run_identifier", sa.String, nullable=False),
        sa.Column(
            "project_entity_id",
            sa.Integer,
            sa.ForeignKey("project_entity.id"),
            nullable=False,
        ),
        sa.UniqueConstraint(
            "provider",
            "run_name",
            "run_identifier",
            "project_entity_id",
            name="uq_batch_identifier_project",
        ),
    )


def downgrade():
    op.drop_constraint("uq_batch_identifier_project", "run_batch_entity")
    op.drop_table("run_batch_entity")
