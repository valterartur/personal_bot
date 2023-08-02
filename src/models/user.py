from sqlalchemy import (
    Column, Integer, String, Index, Boolean
)
from sqlalchemy import func, and_
from sqlalchemy.orm import relationship, aliased

from src.common import Constants
from src.models._base import Base
from src.models.fitness import Exercise, Category, PerformanceData, ForeignKey


class User(Base):
    __tablename__ = Constants.USERS_TABLE

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    display_name = Column(String)
    performance_data = relationship('PerformanceData', backref='user', lazy='dynamic')
    categories = relationship('Category', backref='user', lazy='dynamic')
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    permissions = relationship('Permission', secondary=Constants.USER_PERMISSIONS_TABLE, backref='users')
    gpt_token = relationship('GPTToken', backref='user', uselist=False)
    telegram_user = relationship('TelegramUser', backref='user', uselist=False)

    __table_args__ = (
        Index(f'{Constants.USERS_TABLE}_id_idx', 'id'),
    )

    def latest_category_upload(self, session, category_id: int):
        max_timestamp_for_category = session.query(func.max(PerformanceData.timestamp)).join(
            Exercise,
            PerformanceData.exercise_id == Exercise.id
        ).filter(
            PerformanceData.user_id == self.id,
            Exercise.category_id == category_id
        ).scalar()
        return max_timestamp_for_category

    def user_latest_performance(self, session, category_id: int):
        # TODO: refactor this
        ExerciseAlias = aliased(Exercise)
        CategoryAlias = aliased(Category)

        subquery = (
            session.query(
                PerformanceData.exercise_id,
                func.max(PerformanceData.timestamp).label('max_timestamp')
            ).filter(
                PerformanceData.user_id == self.id,
            ).group_by(PerformanceData.exercise_id).subquery()
        )

        result_query = session.query(PerformanceData, ExerciseAlias, CategoryAlias).join(
            subquery,
            and_(
                PerformanceData.exercise_id == subquery.c.exercise_id,
                PerformanceData.timestamp == subquery.c.max_timestamp
            )
        ).join(
            ExerciseAlias,
            PerformanceData.exercise_id == ExerciseAlias.id
        ).join(
            CategoryAlias,
            and_(
                ExerciseAlias.category_id == CategoryAlias.id,
                CategoryAlias.user_id == self.id,
                CategoryAlias.id == category_id
            )
        ).filter(PerformanceData.timestamp == self.latest_category_upload(session, category_id))
        return result_query


class TelegramUser(Base):
    __tablename__ = Constants.TELEGRAM_USERS_TABLE

    telegram_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    fullname = Column(String)
    chat_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey(f'{Constants.USERS_TABLE}.id'), nullable=False, primary_key=True)

    __table_args__ = (
        Index(f'{Constants.TELEGRAM_USERS_TABLE}_telegram_id_idx', 'telegram_id'),
        Index(f'{Constants.TELEGRAM_USERS_TABLE}_chat_id_idx', 'chat_id'),
    )


class Permission(Base):
    __tablename__ = Constants.PERMISSIONS_TABLE

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    api_type = Column(String, nullable=False)

    __table_args__ = (
        Index(f'{Constants.PERMISSIONS_TABLE}_id_idx', 'id'),
        Index(f'{Constants.PERMISSIONS_TABLE}_name_idx', 'name'),
    )


class UserPermission(Base):
    __tablename__ = Constants.USER_PERMISSIONS_TABLE

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(f'{Constants.USERS_TABLE}.id'))
    permission_id = Column(Integer, ForeignKey(f'{Constants.PERMISSIONS_TABLE}.id'))

    __table_args__ = (
        Index(f'{Constants.USER_PERMISSIONS_TABLE}_id_idx', 'id'),
        Index(f'{Constants.USER_PERMISSIONS_TABLE}_user_id_idx', 'user_id'),
        Index(f'{Constants.USER_PERMISSIONS_TABLE}_permission_id_idx', 'permission_id'),
    )
