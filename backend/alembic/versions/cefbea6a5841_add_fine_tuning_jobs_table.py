"""Add fine_tuning_jobs table

Revision ID: cefbea6a5841
Revises: eed441c63d1c
Create Date: 2026-08-20 15:41:24.318261

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'cefbea6a5841'
down_revision: Union[str, Sequence[str], None] = 'eed441c63d1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'fine_tuning_jobs',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('model_name', sa.String(length=100), nullable=False),
        sa.Column('dataset_name', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('epochs', sa.Integer(), nullable=True),
        sa.Column('batch_size', sa.Integer(), nullable=True),
        sa.Column('learning_rate', sa.String(length=50), nullable=True),
        sa.Column('metrics', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fine_tuning_jobs_user_id'), 'fine_tuning_jobs', ['user_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_fine_tuning_jobs_user_id'), table_name='fine_tuning_jobs')
    op.drop_table('fine_tuning_jobs')
