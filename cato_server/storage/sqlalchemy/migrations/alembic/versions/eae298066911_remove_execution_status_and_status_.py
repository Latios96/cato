"""remove execution status and status columns

Revision ID: eae298066911
Revises: 90429a77791b
Create Date: 2021-11-20 13:21:11.688856

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "eae298066911"
down_revision = "90429a77791b"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("test_result_entity") as batch_op:
        batch_op.drop_column("execution_status")
        batch_op.drop_column("status")


def downgrade():
    pass
