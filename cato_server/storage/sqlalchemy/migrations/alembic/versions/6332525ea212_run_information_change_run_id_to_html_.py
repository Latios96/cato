"""run_information_change_run_id_to_html_url

Revision ID: 6332525ea212
Revises: 118a4e309207
Create Date: 2022-09-26 16:52:13.797719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6332525ea212"
down_revision = "118a4e309207"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("github_actions_run_information_entity") as batch_op:
        batch_op.drop_column("job_id")

    with op.batch_alter_table(
        "github_actions_run_information_entity", schema=None
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "html_url",
                sa.String,
                server_default="",
                nullable=False,
            ),
        )


def downgrade():
    pass
