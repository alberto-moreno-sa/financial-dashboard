"""add_portfolio_snapshots_and_upload_history

Revision ID: 034cff1247f1
Revises: 6b57847ed974
Create Date: 2025-12-26 23:26:00.559948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '034cff1247f1'
down_revision: Union[str, None] = '6b57847ed974'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create upload_history table
    op.create_table(
        'upload_history',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('file_hash', sa.String(length=64), nullable=False),
        sa.Column('file_size_bytes', sa.Integer(), nullable=False),
        sa.Column('statement_date', sa.DateTime(), nullable=False),
        sa.Column('account_holder', sa.String(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False),
        sa.Column('upload_ip', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='processed'),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_upload_history_id'), 'upload_history', ['id'], unique=False)
    op.create_index(op.f('ix_upload_history_file_hash'), 'upload_history', ['file_hash'], unique=False)
    op.create_index(op.f('ix_upload_history_statement_date'), 'upload_history', ['statement_date'], unique=False)
    op.create_index(op.f('ix_upload_history_uploaded_at'), 'upload_history', ['uploaded_at'], unique=False)
    op.create_index('idx_user_file_hash', 'upload_history', ['user_id', 'file_hash'], unique=True)
    op.create_index('idx_user_statement_date', 'upload_history', ['user_id', 'statement_date'], unique=False)

    # Create portfolio_snapshots table
    op.create_table(
        'portfolio_snapshots',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('portfolio_id', sa.String(), nullable=False),
        sa.Column('upload_id', sa.String(), nullable=True),
        sa.Column('snapshot_date', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('equity_value', sa.Numeric(precision=15, scale=2), nullable=False, server_default='0.00'),
        sa.Column('fixed_income_value', sa.Numeric(precision=15, scale=2), nullable=False, server_default='0.00'),
        sa.Column('cash_value', sa.Numeric(precision=15, scale=2), nullable=False, server_default='0.00'),
        sa.Column('total_value', sa.Numeric(precision=15, scale=2), nullable=False, server_default='0.00'),
        sa.Column('total_change', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('total_change_percent', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('currency', sa.String(), nullable=False, server_default='MXN'),
        sa.Column('account_holder', sa.String(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['upload_id'], ['upload_history.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_portfolio_snapshots_id'), 'portfolio_snapshots', ['id'], unique=False)
    op.create_index(op.f('ix_portfolio_snapshots_portfolio_id'), 'portfolio_snapshots', ['portfolio_id'], unique=False)
    op.create_index(op.f('ix_portfolio_snapshots_upload_id'), 'portfolio_snapshots', ['upload_id'], unique=False)
    op.create_index(op.f('ix_portfolio_snapshots_snapshot_date'), 'portfolio_snapshots', ['snapshot_date'], unique=False)
    op.create_index('idx_portfolio_snapshot_date', 'portfolio_snapshots', ['portfolio_id', 'snapshot_date'], unique=True)

    # Create snapshot_positions table
    op.create_table(
        'snapshot_positions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('snapshot_id', sa.String(), nullable=False),
        sa.Column('ticker', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('asset_type', sa.String(), nullable=True, server_default='Stock'),
        sa.Column('quantity', sa.Numeric(precision=15, scale=4), nullable=False),
        sa.Column('avg_cost', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('current_price', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('market_value', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('unrealized_gain', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('unrealized_gain_percent', sa.Numeric(precision=8, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['snapshot_id'], ['portfolio_snapshots.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_snapshot_positions_id'), 'snapshot_positions', ['id'], unique=False)
    op.create_index(op.f('ix_snapshot_positions_snapshot_id'), 'snapshot_positions', ['snapshot_id'], unique=False)
    op.create_index(op.f('ix_snapshot_positions_ticker'), 'snapshot_positions', ['ticker'], unique=False)
    op.create_index('idx_snapshot_ticker', 'snapshot_positions', ['snapshot_id', 'ticker'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index('idx_snapshot_ticker', table_name='snapshot_positions')
    op.drop_index(op.f('ix_snapshot_positions_ticker'), table_name='snapshot_positions')
    op.drop_index(op.f('ix_snapshot_positions_snapshot_id'), table_name='snapshot_positions')
    op.drop_index(op.f('ix_snapshot_positions_id'), table_name='snapshot_positions')
    op.drop_table('snapshot_positions')

    op.drop_index('idx_portfolio_snapshot_date', table_name='portfolio_snapshots')
    op.drop_index(op.f('ix_portfolio_snapshots_snapshot_date'), table_name='portfolio_snapshots')
    op.drop_index(op.f('ix_portfolio_snapshots_upload_id'), table_name='portfolio_snapshots')
    op.drop_index(op.f('ix_portfolio_snapshots_portfolio_id'), table_name='portfolio_snapshots')
    op.drop_index(op.f('ix_portfolio_snapshots_id'), table_name='portfolio_snapshots')
    op.drop_table('portfolio_snapshots')

    op.drop_index('idx_user_statement_date', table_name='upload_history')
    op.drop_index('idx_user_file_hash', table_name='upload_history')
    op.drop_index(op.f('ix_upload_history_uploaded_at'), table_name='upload_history')
    op.drop_index(op.f('ix_upload_history_statement_date'), table_name='upload_history')
    op.drop_index(op.f('ix_upload_history_file_hash'), table_name='upload_history')
    op.drop_index(op.f('ix_upload_history_id'), table_name='upload_history')
    op.drop_table('upload_history')
