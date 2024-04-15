"""migrate deduplicating file storage

Revision ID: 69dfb56b8927
Revises: a56f63de66a9
Create Date: 2020-12-11 20:46:32.575899

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "69dfb56b8927"
down_revision = "a56f63de66a9"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("UPDATE FILE_ENTITY SET VALUE_COUNTER = 0")


def downgrade():
    pass
