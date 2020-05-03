"""init

Revision ID: 533bb8c681be
Revises: 
Create Date: 2020-05-03 22:04:49.501278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '533bb8c681be'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('doku_stylesheet',
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('source', sa.UnicodeText(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('doku_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=48), nullable=False),
    sa.Column('email', sa.String(length=48), nullable=False),
    sa.Column('password', sa.LargeBinary(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('doku_template',
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('base_style_id', sa.Integer(), nullable=True),
    sa.Column('source', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['base_style_id'], ['doku_stylesheet.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('doku_document',
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['template_id'], ['doku_template.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('doku_template_stylesheet_relation',
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('style_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['style_id'], ['doku_stylesheet.id'], ),
    sa.ForeignKeyConstraint(['template_id'], ['doku_template.id'], )
    )
    op.create_table('doku_variable',
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('use_markdown', sa.Boolean(), nullable=True),
    sa.Column('css_class', sa.String(length=255), nullable=True),
    sa.Column('content', sa.UnicodeText(), nullable=False),
    sa.Column('compiled_content', sa.UnicodeText(), nullable=False),
    sa.Column('document_id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['doku_document.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['doku_variable.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('doku_variable')
    op.drop_table('doku_template_stylesheet_relation')
    op.drop_table('doku_document')
    op.drop_table('doku_template')
    op.drop_table('doku_user')
    op.drop_table('doku_stylesheet')
    # ### end Alembic commands ###
