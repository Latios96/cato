"""remove hashed_password

Revision ID: f97c81a691c2
Revises: addb5694cd1b
Create Date: 2022-03-01 13:44:12.194904

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "f97c81a691c2"
down_revision = "addb5694cd1b"
branch_labels = None
depends_on = None


def upgrade():
    if "sqlite" in op.get_bind().engine.driver:
        with op.batch_alter_table("user_entity") as batch_op:
            batch_op.drop_column("hashed_password")

        op.execute("CREATE UNIQUE INDEX uq_username on user_entity (LOWER(username));")
    else:
        op.execute("ALTER TABLE user_entity DROP COLUMN hashed_password")


def downgrade():
    pass
