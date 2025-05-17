"""Crear tabla clientes_corredores

Revision ID: 2025_05_17_0554
Revises: 
Create Date: 2025-05-17 05:54:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Identificador de revisión
revision = '2025_05_17_0554'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Crear la tabla clientes_corredores
    op.create_table(
        'clientes_corredores',
        sa.Column('cliente_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('corredor_numero', sa.Integer(), nullable=False),
        sa.Column('fecha_asignacion', sa.Date(), nullable=False, server_default=sa.text('CURRENT_DATE')),
        sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['corredor_numero'], ['corredores.numero'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('cliente_id', 'corredor_numero')
    )
    
    # Crear índices para mejorar el rendimiento de las consultas
    op.create_index(op.f('ix_clientes_corredores_cliente_id'), 'clientes_corredores', ['cliente_id'], unique=False)
    op.create_index(op.f('ix_clientes_corredores_corredor_numero'), 'clientes_corredores', ['corredor_numero'], unique=False)


def downgrade():
    # Eliminar índices
    op.drop_index(op.f('ix_clientes_corredores_corredor_numero'), table_name='clientes_corredores')
    op.drop_index(op.f('ix_clientes_corredores_cliente_id'), table_name='clientes_corredores')
    
    # Eliminar la tabla
    op.drop_table('clientes_corredores')
