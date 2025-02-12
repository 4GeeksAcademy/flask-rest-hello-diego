"""empty message

Revision ID: f16dc9171867
Revises: 
Create Date: 2025-01-31 20:25:10.047839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f16dc9171867'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('height', sa.String(length=50), nullable=True),
    sa.Column('mass', sa.String(length=50), nullable=True),
    sa.Column('hair_color', sa.String(length=50), nullable=True),
    sa.Column('skin_color', sa.String(length=50), nullable=True),
    sa.Column('eye_color', sa.String(length=50), nullable=True),
    sa.Column('birth_year', sa.String(length=50), nullable=True),
    sa.Column('gender', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('climate', sa.String(length=250), nullable=True),
    sa.Column('terrain', sa.String(length=250), nullable=True),
    sa.Column('population', sa.String(length=250), nullable=True),
    sa.Column('diameter', sa.String(length=250), nullable=True),
    sa.Column('rotation_period', sa.String(length=250), nullable=True),
    sa.Column('orbital_period', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('starships',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('model', sa.String(length=250), nullable=True),
    sa.Column('manufacturer', sa.String(length=250), nullable=True),
    sa.Column('cost_in_credits', sa.String(length=50), nullable=True),
    sa.Column('length', sa.String(length=50), nullable=True),
    sa.Column('crew', sa.String(length=50), nullable=True),
    sa.Column('passengers', sa.String(length=50), nullable=True),
    sa.Column('max_atmosphering_speed', sa.String(length=50), nullable=True),
    sa.Column('hyperdrive_rating', sa.String(length=50), nullable=True),
    sa.Column('starship_class', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('favorite_type', sa.Enum('PEOPLE', 'PLANET', 'STARSHIP', name='favoritetype'), nullable=False),
    sa.Column('favorite_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorites')
    op.drop_table('users')
    op.drop_table('starships')
    op.drop_table('planets')
    op.drop_table('people')
    # ### end Alembic commands ###
