"""Init

Revision ID: 0e54042fdba6
Revises: 
Create Date: 2023-07-23 20:08:00.179149

"""
from alembic import op
import sqlalchemy as sa
import src

# revision identifiers, used by Alembic.
revision = '0e54042fdba6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gpt_model_dim',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('model', sa.String(), nullable=True),
    sa.Column('display_name', sa.String(), nullable=True),
    sa.Column('model_type', sa.String(), nullable=True),
    sa.Column('input_type', sa.String(), nullable=True),
    sa.Column('cost', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('permissions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('api_type', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('permissions_id_idx', 'permissions', ['id'], unique=False)
    op.create_index('permissions_name_idx', 'permissions', ['name'], unique=False)
    op.create_table('user_dim',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('display_name', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('user_dim_id_idx', 'user_dim', ['id'], unique=False)
    op.create_table('category_dim',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('display_name', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_dim.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('category_dim_id_idx', 'category_dim', ['id'], unique=False)
    op.create_table('gpt_token_dim',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('token', src.lib.sa_columns.encrypted_column.EncryptedString(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_dim.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('gpt_token_dim_id_idx', 'gpt_token_dim', ['id'], unique=False)
    op.create_index('gpt_token_dim_user_id_idx', 'gpt_token_dim', ['user_id'], unique=False)
    op.create_table('telegram_user_dim',
    sa.Column('telegram_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('fullname', sa.String(), nullable=True),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_dim.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index('telegram_user_dim_chat_id_idx', 'telegram_user_dim', ['chat_id'], unique=False)
    op.create_index('telegram_user_dim_telegram_id_idx', 'telegram_user_dim', ['telegram_id'], unique=False)
    op.create_table('user_permissions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('permission_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_dim.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('user_permissions_id_idx', 'user_permissions', ['id'], unique=False)
    op.create_index('user_permissions_permission_id_idx', 'user_permissions', ['permission_id'], unique=False)
    op.create_index('user_permissions_user_id_idx', 'user_permissions', ['user_id'], unique=False)
    op.create_table('exercise_dim',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('display_name', sa.String(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category_dim.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('exercise_dim_category_id_idx', 'exercise_dim', ['category_id'], unique=False)
    op.create_index('exercise_dim_id_idx', 'exercise_dim', ['id'], unique=False)
    op.create_table('gpt_conversation_fact',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('token_id', sa.Integer(), nullable=True),
    sa.Column('billing', sa.Integer(), nullable=True),
    sa.Column('start', sa.DateTime(), nullable=True),
    sa.Column('end', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['token_id'], ['gpt_token_dim.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_dim.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('gpt_conversation_fact_id_idx', 'gpt_conversation_fact', ['id'], unique=False)
    op.create_index('gpt_conversation_fact_token_id_idx', 'gpt_conversation_fact', ['token_id'], unique=False)
    op.create_index('gpt_conversation_fact_user_id_idx', 'gpt_conversation_fact', ['user_id'], unique=False)
    op.create_table('gpt_audit_dim',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('model_id', sa.Integer(), nullable=True),
    sa.Column('conversation_id', sa.Integer(), nullable=True),
    sa.Column('prompt', sa.String(), nullable=True),
    sa.Column('response', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('previous_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['conversation_id'], ['gpt_conversation_fact.id'], ),
    sa.ForeignKeyConstraint(['model_id'], ['gpt_model_dim.id'], ),
    sa.ForeignKeyConstraint(['previous_id'], ['gpt_audit_dim.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('gpt_audit_dim_conversation_id_idx', 'gpt_audit_dim', ['conversation_id'], unique=False)
    op.create_index('gpt_audit_dim_id_idx', 'gpt_audit_dim', ['id'], unique=False)
    op.create_index('gpt_audit_dim_model_id_idx', 'gpt_audit_dim', ['model_id'], unique=False)
    op.create_index('gpt_audit_dim_previous_id_idx', 'gpt_audit_dim', ['previous_id'], unique=False)
    op.create_index('gpt_audit_dim_timestamp_idx', 'gpt_audit_dim', ['timestamp'], unique=False)
    op.create_table('performance_data_fact',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('sets', sa.Integer(), nullable=False),
    sa.Column('reps', sa.JSON(), nullable=False),
    sa.Column('weight', sa.JSON(), nullable=False),
    sa.Column('timestamp', sa.Date(), nullable=False),
    sa.Column('exercise_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercise_dim.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_dim.id'], ),
    sa.PrimaryKeyConstraint('timestamp', 'exercise_id')
    )
    op.create_index('pd_exercise_id_idx', 'performance_data_fact', ['exercise_id'], unique=False)
    op.create_index('pd_exercise_id_timestamp_idx', 'performance_data_fact', ['exercise_id', 'timestamp'], unique=False)
    op.create_index('pd_timestamp_idx', 'performance_data_fact', ['timestamp'], unique=False)
    op.create_index('pd_user_id_idx', 'performance_data_fact', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('pd_user_id_idx', table_name='performance_data_fact')
    op.drop_index('pd_timestamp_idx', table_name='performance_data_fact')
    op.drop_index('pd_exercise_id_timestamp_idx', table_name='performance_data_fact')
    op.drop_index('pd_exercise_id_idx', table_name='performance_data_fact')
    op.drop_table('performance_data_fact')
    op.drop_index('gpt_audit_dim_timestamp_idx', table_name='gpt_audit_dim')
    op.drop_index('gpt_audit_dim_previous_id_idx', table_name='gpt_audit_dim')
    op.drop_index('gpt_audit_dim_model_id_idx', table_name='gpt_audit_dim')
    op.drop_index('gpt_audit_dim_id_idx', table_name='gpt_audit_dim')
    op.drop_index('gpt_audit_dim_conversation_id_idx', table_name='gpt_audit_dim')
    op.drop_table('gpt_audit_dim')
    op.drop_index('gpt_conversation_fact_user_id_idx', table_name='gpt_conversation_fact')
    op.drop_index('gpt_conversation_fact_token_id_idx', table_name='gpt_conversation_fact')
    op.drop_index('gpt_conversation_fact_id_idx', table_name='gpt_conversation_fact')
    op.drop_table('gpt_conversation_fact')
    op.drop_index('exercise_dim_id_idx', table_name='exercise_dim')
    op.drop_index('exercise_dim_category_id_idx', table_name='exercise_dim')
    op.drop_table('exercise_dim')
    op.drop_index('user_permissions_user_id_idx', table_name='user_permissions')
    op.drop_index('user_permissions_permission_id_idx', table_name='user_permissions')
    op.drop_index('user_permissions_id_idx', table_name='user_permissions')
    op.drop_table('user_permissions')
    op.drop_index('telegram_user_dim_telegram_id_idx', table_name='telegram_user_dim')
    op.drop_index('telegram_user_dim_chat_id_idx', table_name='telegram_user_dim')
    op.drop_table('telegram_user_dim')
    op.drop_index('gpt_token_dim_user_id_idx', table_name='gpt_token_dim')
    op.drop_index('gpt_token_dim_id_idx', table_name='gpt_token_dim')
    op.drop_table('gpt_token_dim')
    op.drop_index('category_dim_id_idx', table_name='category_dim')
    op.drop_table('category_dim')
    op.drop_index('user_dim_id_idx', table_name='user_dim')
    op.drop_table('user_dim')
    op.drop_index('permissions_name_idx', table_name='permissions')
    op.drop_index('permissions_id_idx', table_name='permissions')
    op.drop_table('permissions')
    op.drop_table('gpt_model_dim')
    # ### end Alembic commands ###
