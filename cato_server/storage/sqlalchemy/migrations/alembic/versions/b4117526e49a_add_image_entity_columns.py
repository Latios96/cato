"""add image entity columns

Revision ID: b4117526e49a
Revises: 37ee8dba5560
Create Date: 2020-12-12 19:39:56.622169

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import orm

from cato_server.storage.sqlalchemy.sqlalchemy_image_repository import (
    ImageMapping,
    ImageChannelMapping,
)
from cato_server.storage.sqlalchemy.sqlalchemy_simple_file_storage import _FileMapping
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    _TestResultMapping,
)

revision = "b4117526e49a"
down_revision = "37ee8dba5560"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("test_result_entity", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "image_output_id",
                sa.Integer(),
                sa.ForeignKey("image_entity.id", name="image_output_id_fk"),
            ),
        )
        batch_op.add_column(
            sa.Column(
                "reference_image_id",
                sa.Integer(),
                sa.ForeignKey("image_entity.id", name="reference_image_id_fk"),
            ),
        )
    conn = op.get_bind()
    res = conn.execute(
        "select id, image_output, reference_image from test_result_entity"
    )
    results = res.fetchall()

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    for id, image_output, reference_image in results:
        if image_output:
            name = (
                session.query(_FileMapping)
                .filter(_FileMapping.id == image_output)
                .first()
                .name
            )
            image = ImageMapping(
                id=None,
                name=name,
                original_file_entity_id=image_output,
                channels=[
                    ImageChannelMapping(
                        id=None,
                        image_entity_id=None,
                        name=name,
                        file_entity_id=image_output,
                    )
                ],
            )
            session.add(image)
            session.commit()
            test_result = (
                session.query(_TestResultMapping)
                .filter(_TestResultMapping.id == id)
                .first()
            )
            test_result.image_output_id = image.id
            session.merge(test_result)
            session.commit()

        if reference_image:
            name = (
                session.query(_FileMapping)
                .filter(_FileMapping.id == reference_image)
                .first()
                .name
            )
            image = ImageMapping(
                id=None,
                name=name,
                original_file_entity_id=reference_image,
                channels=[
                    ImageChannelMapping(
                        id=None,
                        image_entity_id=None,
                        name="rgb",
                        file_entity_id=reference_image,
                    )
                ],
            )
            session.add(image)
            session.commit()
            test_result = (
                session.query(_TestResultMapping)
                .filter(_TestResultMapping.id == id)
                .first()
            )
            test_result.reference_image_id = image.id
            session.merge(test_result)
            session.commit()

    session.commit()


def downgrade():
    with op.batch_alter_table("file_entity") as batch_op:
        batch_op.drop_column("image_output_id")
        batch_op.drop_column("reference_image_id")
