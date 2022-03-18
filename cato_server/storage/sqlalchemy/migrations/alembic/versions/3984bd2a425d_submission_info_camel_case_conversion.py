"""submission_info_camel_case_conversion

Revision ID: 3984bd2a425d
Revises: 9bf8a029dc0e
Create Date: 2022-03-17 17:00:27.742001

"""
import json

from alembic import op


# revision identifiers, used by Alembic.
from caseconverter import camelcase

revision = "3984bd2a425d"
down_revision = "9bf8a029dc0e"
branch_labels = None
depends_on = None


def _case_convert_dict(data):
    d = {}
    for key, value in data.items():
        if isinstance(value, dict):
            d[camelcase(key)] = _case_convert_dict(value)
        elif isinstance(value, list):
            d[camelcase(key)] = [_case_convert_dict(x) for x in value]
        else:
            d[camelcase(key)] = value
    return d


def upgrade():
    conn = op.get_bind()

    submission_infos = conn.execute(
        "select id,config from submission_info_entity"
    ).fetchall()
    for (submission_info_id, submission_info) in submission_infos:
        data = (
            json.loads(submission_info)
            if not isinstance(submission_info, dict)
            else submission_info
        )
        converted_data = _case_convert_dict(data)
        converted_submission_info = json.dumps(converted_data)
        conn.execute(
            f"UPDATE submission_info_entity SET config='{converted_submission_info}' where id={submission_info_id}"
        )


def downgrade():
    pass
