"""Create tracked_items and buy_it_now_averages tables

Revision ID: 67c92525e264
Revises: 
Create Date: 2025-08-05 19:25:58.906032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67c92525e264'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create tracked_items table
    op.create_table(
        'tracked_items',
        sa.Column('id', sa.String, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('current_price', sa.Float, nullable=False),
        sa.Column('end_time', sa.DateTime, nullable=False),
        sa.Column('upc', sa.String, nullable=True),
        sa.Column('ean', sa.String, nullable=True),
        sa.Column('gtin', sa.String, nullable=True),
        sa.Column('category_id', sa.String, nullable=True),
        sa.Column('last_checked', sa.DateTime, nullable=False)
    )

    # Create buy_it_now_averages table
    op.create_table(
        'buy_it_now_averages',
        sa.Column('item_type', sa.String, primary_key=True),
        sa.Column('average_price', sa.Float, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop buy_it_now_averages table
    op.drop_table('buy_it_now_averages')

    # Drop tracked_items table
    op.drop_table('tracked_items')
