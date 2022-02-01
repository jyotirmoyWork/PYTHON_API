"""add last few column in post

Revision ID: fcda3e21ec45
Revises: 05ca33bb5ff8
Create Date: 2022-02-01 16:05:28.247955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcda3e21ec45'
down_revision = '05ca33bb5ff8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("POSTS", sa.Column(
        "PUBLISHED", sa.Boolean(), nullable=False, server_default="TRUE"),)
    op.add_column("POSTS", sa.Column(
        "CREATED_AT", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")
    ),)
    pass


def downgrade():
    op.drop_column("POSTS", "PUBLISHED")
    op.drop_column("POSTS", "CREATED_AT")
    pass
