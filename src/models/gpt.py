from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, Boolean, Float
from sqlalchemy.orm import relationship, backref

from src.common import Constants
from src.lib.sa_columns import EncryptedString
from src.models._base import Base


class GPTToken(Base):
    __tablename__ = Constants.GPT_TOKEN_TABLE

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(EncryptedString)
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey(f'{Constants.USERS_TABLE}.id'))
    audit_records = relationship('GPTConversation', backref='token')

    __table_args__ = (
        Index(f'{Constants.GPT_TOKEN_TABLE}_id_idx', 'id'),
        Index(f'{Constants.GPT_TOKEN_TABLE}_user_id_idx', 'user_id'),
    )


class GPTConversation(Base):
    __tablename__ = Constants.GPT_CONVERSATION_TABLE

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(f'{Constants.USERS_TABLE}.id'))
    token_id = Column(Integer, ForeignKey(f'{Constants.GPT_TOKEN_TABLE}.id'))
    total_billing = Column(Float, nullable=True)
    start = Column(DateTime, default=datetime.utcnow)
    end = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    messages = relationship('GPTAudit', backref='conversation')

    __table_args__ = (
        Index(f'{Constants.GPT_CONVERSATION_TABLE}_id_idx', 'id'),
        Index(f'{Constants.GPT_CONVERSATION_TABLE}_user_id_idx', 'user_id'),
        Index(f'{Constants.GPT_CONVERSATION_TABLE}_token_id_idx', 'token_id'),
    )


class GPTAudit(Base):
    __tablename__ = Constants.GPT_AUDIT_TABLE

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey(f'{Constants.GPT_MODEL_TABLE}.id'))
    conversation_id = Column(Integer, ForeignKey(f'{Constants.GPT_CONVERSATION_TABLE}.id'))
    prompt = Column(String, nullable=True)
    response = Column(String, nullable=True)
    billing = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    previous_id = Column(Integer, ForeignKey(f'{Constants.GPT_AUDIT_TABLE}.id'))
    previous = relationship('GPTAudit', backref=backref('next', uselist=False), remote_side=[id])
    model = relationship('GPTModel', backref='audit_records')

    __table_args__ = (
        Index(f'{Constants.GPT_AUDIT_TABLE}_id_idx', 'id'),
        Index(f'{Constants.GPT_AUDIT_TABLE}_model_id_idx', 'model_id'),
        Index(f'{Constants.GPT_AUDIT_TABLE}_conversation_id_idx', 'conversation_id'),
        Index(f'{Constants.GPT_AUDIT_TABLE}_previous_id_idx', 'previous_id'),
        Index(f'{Constants.GPT_AUDIT_TABLE}_timestamp_idx', 'timestamp'),
    )


class GPTModel(Base):
    __tablename__ = Constants.GPT_MODEL_TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(String)
    display_name = Column(String)
    model_type = Column(String)
    input_type = Column(String)
    cost = Column(Float)



