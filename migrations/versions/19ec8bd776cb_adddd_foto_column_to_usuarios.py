"""add foto column to usuarios

Revision ID: 19ec8bd776cb
Revises: 
Create Date: 2025-10-23 15:37:05.348436
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '19ec8bd776cb'
down_revision = None  # mantém None se for a primeira migração
branch_labels = None
depends_on = None


def upgrade():
    # Adiciona a coluna 'foto' na tabela 'usuarios'
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('foto', sa.String(length=255), nullable=True))


def downgrade():
    # Remove a coluna 'foto' da tabela 'usuarios'
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.drop_column('foto')
