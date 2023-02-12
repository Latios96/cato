"""fix_nans_in_test_result_edits

Revision ID: cf66bbdc5901
Revises: 9a2d397907ef
Create Date: 2023-02-12 19:34:45.194766

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "cf66bbdc5901"
down_revision = "9a2d397907ef"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "UPDATE reference_image_edit_entity set new_error_value=1 where new_error_value ='NaN'"
    )


def downgrade():
    pass
