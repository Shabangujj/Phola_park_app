"""Add survey details and committee table

Revision ID: a748c9395b1d
Revises: 402214a21c67
Create Date: 2026-06-04 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a748c9395b1d'
down_revision = '402214a21c67'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('surveys', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('surveys', sa.Column('link', sa.String(length=255), nullable=True))
    op.add_column('surveys', sa.Column('portfolio', sa.String(length=50), nullable=True))

    op.create_table(
        'committees',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('portfolio', sa.String(length=50), nullable=False),
        sa.Column('created_by', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_table('committees')
    op.drop_column('surveys', 'portfolio')
    op.drop_column('surveys', 'link')
    op.drop_column('surveys', 'description')
