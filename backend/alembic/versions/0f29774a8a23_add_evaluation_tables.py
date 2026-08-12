"""Add evaluation tables

Revision ID: 0f29774a8a23
Revises: 9f9370e5431d
Create Date: 2026-08-12 10:41:20.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0f29774a8a23'
down_revision: Union[str, Sequence[str], None] = '9f9370e5431d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('eval_suites',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_eval_suites_user_id'), 'eval_suites', ['user_id'], unique=False)

    op.create_table('eval_test_cases',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('suite_id', sa.String(length=36), nullable=False),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('expected_output', sa.Text(), nullable=True),
        sa.Column('assertion_type', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['suite_id'], ['eval_suites.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_eval_test_cases_suite_id'), 'eval_test_cases', ['suite_id'], unique=False)

    op.create_table('eval_runs',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('suite_id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('model', sa.String(length=100), nullable=False),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('passed_count', sa.Integer(), nullable=False),
        sa.Column('failed_count', sa.Integer(), nullable=False),
        sa.Column('total_count', sa.Integer(), nullable=False),
        sa.Column('results', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['suite_id'], ['eval_suites.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_eval_runs_suite_id'), 'eval_runs', ['suite_id'], unique=False)
    op.create_index(op.f('ix_eval_runs_user_id'), 'eval_runs', ['user_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_eval_runs_user_id'), table_name='eval_runs')
    op.drop_index(op.f('ix_eval_runs_suite_id'), table_name='eval_runs')
    op.drop_table('eval_runs')
    op.drop_index(op.f('ix_eval_test_cases_suite_id'), table_name='eval_test_cases')
    op.drop_table('eval_test_cases')
    op.drop_index(op.f('ix_eval_suites_user_id'), table_name='eval_suites')
    op.drop_table('eval_suites')
