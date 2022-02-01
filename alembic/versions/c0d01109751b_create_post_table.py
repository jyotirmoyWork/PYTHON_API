"""create post table

Revision ID: c0d01109751b
Revises: 
Create Date: 2022-02-01 15:31:26.627080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0d01109751b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("POSTS", sa.Column("ID", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("TITLE", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table("POSTS")
    pass
