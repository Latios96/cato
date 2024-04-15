"""add output entity

Revision ID: f6913d2c7757
Revises: 04fc7a4a1902
Create Date: 2020-12-07 12:28:13.069833

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f6913d2c7757"
down_revision = "04fc7a4a1902"
branch_labels = None
depends_on = None


def upgrade():
    output_table = op.create_table(
        "output_entity",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "test_result_entity_id",
            sa.INTEGER,
            sa.ForeignKey("test_result_entity.id"),
            unique=True,
        ),
        sa.Column("text", sa.Text(), nullable=False),
    )
    conn = op.get_bind()
    res = conn.execute("select id, output from test_result_entity")
    results = res.fetchall()

    output_data = [
        {"test_result_entity_id": r[0], "text": "".join(r[1])} for r in results
    ]

    op.bulk_insert(output_table, output_data)


def downgrade():
    op.drop_table("output_entity")
