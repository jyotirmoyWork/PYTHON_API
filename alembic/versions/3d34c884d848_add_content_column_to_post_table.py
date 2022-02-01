"""add content column to post table

Revision ID: 3d34c884d848
Revises: c0d01109751b
Create Date: 2022-02-01 15:50:37.403617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d34c884d848'
down_revision = 'c0d01109751b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("POSTS", sa.Column("CONTENT", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("POSTS", "CONTENT")
    pass
