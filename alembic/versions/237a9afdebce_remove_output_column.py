"""remove output column

Revision ID: 237a9afdebce
Revises: f6913d2c7757
Create Date: 2020-12-07 13:12:25.483491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "237a9afdebce"
down_revision = "f6913d2c7757"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("test_result_entity", "output")


def downgrade():
    pass
