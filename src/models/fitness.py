from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Index, ForeignKey, Date, JSON
)
from sqlalchemy.orm import relationship

from src.common import Constants
from src.models._base import Base


class PerformanceData(Base):
    __tablename__ = Constants.PERFORMANCE_DATA_TABLE

    user_id = Column(Integer, ForeignKey('user_dim.id'), nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(JSON, nullable=False)
    weight = Column(JSON, nullable=False)
    timestamp = Column(Date(), default=datetime.date, primary_key=True)
    exercise_id = Column(Integer, ForeignKey('exercise_dim.id'), nullable=False, primary_key=True)

    __table_args__ = (
        Index('pd_user_id_idx', 'user_id'),
        Index('pd_exercise_id_idx', 'exercise_id'),
        Index('pd_timestamp_idx', 'timestamp'),
        Index('pd_exercise_id_timestamp_idx', 'exercise_id', 'timestamp'),
    )


class Category(Base):
    __tablename__ = Constants.CATEGORIES_TABLE

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    display_name = Column(String)
    exercises = relationship('Exercise', backref='category', lazy='dynamic')
    user_id = Column(Integer, ForeignKey('user_dim.id'), nullable=False)

    __table_args__ = (
        Index(f'{Constants.CATEGORIES_TABLE}_id_idx', 'id'),
    )


class Exercise(Base):
    __tablename__ = Constants.EXCERSISES_TABLE

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    display_name = Column(String)
    category_id = Column(Integer, ForeignKey('category_dim.id'), nullable=False)
    performance_data = relationship('PerformanceData', backref='exercise', lazy='dynamic')

    __table_args__ = (
        Index(f'{Constants.EXCERSISES_TABLE}_id_idx', 'id'),
        Index(f'{Constants.EXCERSISES_TABLE}_category_id_idx', 'category_id'),
    )



