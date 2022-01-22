"""create datasets table

Revision ID: 5accf51d2fde
Revises: 
Create Date: 2022-01-22 13:08:45.037985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5accf51d2fde'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'datasets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('storage_platform', sa.String(50), nullable=False),
        sa.Column('notification_email', sa.String(100))
    )


def downgrade():
    op.drop_table('datasets')
