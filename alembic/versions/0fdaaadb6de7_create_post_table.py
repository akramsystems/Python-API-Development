"""Create Post Table

Revision ID: 0fdaaadb6de7
Revises: 
Create Date: 2022-05-15 15:19:17.426612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fdaaadb6de7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # put logic for upgrade or making additive changes
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("title", sa.String, nullable=False)
    )


def downgrade():
    # Put logic for rolling back or making subtractive changes
    op.drop_table("posts")
