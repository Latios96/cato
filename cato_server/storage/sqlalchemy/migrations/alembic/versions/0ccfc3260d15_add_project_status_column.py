"""add_project_status_column

Revision ID: 0ccfc3260d15
Revises: 08647723aa61
Create Date: 2024-05-09 15:14:30.772683

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0ccfc3260d15"
down_revision = "08647723aa61"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("project_entity", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("status", sa.String(), nullable=True),
        )

    op.execute("update project_entity set status='ACTIVE'")

    with op.batch_alter_table("project_entity") as batch_op:
        batch_op.alter_column("status", existing_type=sa.String(), nullable=False)


def downgrade():
    with op.batch_alter_table("project_entity") as batch_op:
        batch_op.drop_column("state")
