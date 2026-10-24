"""merge articles and search_vector

Revision ID: e6914b6f3129
Revises: 1235ce059e46, f9d377da3f22
Create Date: 2026-10-24 17:59:34.927138

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6914b6f3129'
down_revision: Union[str, Sequence[str], None] = ('1235ce059e46', 'f9d377da3f22')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
