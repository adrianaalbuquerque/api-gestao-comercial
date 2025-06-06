"""create table clients

Revision ID: fffed557cf94
Revises: 279a1b9cace3
Create Date: 2025-05-27 12:27:21.485994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fffed557cf94'
down_revision: Union[str, None] = '279a1b9cace3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('client_cpf', sa.String(length=14), nullable=False),
    sa.Column('client_email', sa.String(length=100), nullable=False),
    sa.Column('client_name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('client_cpf'),
    sa.UniqueConstraint('client_email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clients')
    # ### end Alembic commands ###
