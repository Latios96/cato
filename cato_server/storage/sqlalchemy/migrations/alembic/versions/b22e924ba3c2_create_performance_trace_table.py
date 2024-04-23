"""create performance trace table

Revision ID: b22e924ba3c2
Revises: cf66bbdc5901
Create Date: 2024-04-23 13:47:04.945129

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "b22e924ba3c2"
down_revision = "cf66bbdc5901"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "performance_trace_entity",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("performance_trace_json", sa.Text),
    )
    with op.batch_alter_table("run_entity", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "performance_trace_entity_id",
                sa.INTEGER,
                sa.ForeignKey(
                    "performance_trace_entity.id",
                    name="performance_trace_entity_id_fk",
                ),
                nullable=True,
            ),
        )


def downgrade():
    op.drop_table("performance_trace_entity")

    with op.batch_alter_table("run_entity") as batch_op:
        batch_op.drop_column("performance_trace_entity_id")
