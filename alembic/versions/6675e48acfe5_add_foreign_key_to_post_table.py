"""add foreign key to post table

Revision ID: 6675e48acfe5
Revises: 6593cf870d78
Create Date: 2022-05-21 15:03:02.164731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6675e48acfe5'
down_revision = '6593cf870d78'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )


def downgrade():
    op.drop_constraint("post_users_fk", table_name="post")
    op.drop_column(table_name="post", column_name="owner_id")
