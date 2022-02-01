"""add forenkey to post table

Revision ID: 05ca33bb5ff8
Revises: 4032337da7b1
Create Date: 2022-02-01 15:59:23.090668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05ca33bb5ff8'
down_revision = '4032337da7b1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("POSTS", sa.Column("OWNER_ID",sa.Integer(), nullable=False))
    op.create_foreign_key("POST_USERS_FK", source_table="POSTS", referent_table="USERS", local_cols=["OWNER_ID"], remote_cols=["ID"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("POST_USERS_FK", table_name="POSTS")
    op.drop_column("POSTS", "CONTENT")
    pass
