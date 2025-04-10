"""empty message

Revision ID: 6e6eedfcb62e
Revises: 
Create Date: 2025-03-31 17:23:14.198577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e6eedfcb62e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=200), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=True),
    sa.Column('password_hash', sa.String(length=100), nullable=True),
    sa.Column('create', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('expenses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('category', sa.String(length=200), nullable=True),
    sa.Column('budget', sa.Float(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('category')
    )
    op.create_table('budget',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('expenses_id', sa.Integer(), nullable=True),
    sa.Column('expenses_type', sa.String(length=400), nullable=True),
    sa.Column('category', sa.String(length=200), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('marchant', sa.String(length=300), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['expenses_id'], ['expenses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('total_budget',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('budget_id', sa.Integer(), nullable=True),
    sa.Column('monthly_budget', sa.Integer(), nullable=True),
    sa.Column('Total_in_week', sa.Integer(), nullable=True),
    sa.Column('Total_in_Month', sa.Integer(), nullable=True),
    sa.Column('Total_in_3months', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['budget_id'], ['budget.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('total_budget')
    op.drop_table('budget')
    op.drop_table('expenses')
    op.drop_table('user')
    # ### end Alembic commands ###
