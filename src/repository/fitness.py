from src.models.fitness import (
    Category,
    Exercise,
    PerformanceData,
)
from src.repository._base import BaseRepository


class CategoryRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(model=Category, session=session)

    def store_from_name(self, name: str, user_id: int) -> Category:
        return self.save(name=name.lower().replace(' ', '_'), display_name=name, user_id=user_id)


class ExerciseRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(model=Exercise, session=session)

    def store_from_name(self, name: str, category_id: int) -> Exercise:
        return self.save(
            name=name.lower().replace(' ', '_'),
            display_name=name,
            category_id=category_id,
        )


class PerformanceDataRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(model=PerformanceData, session=session)

    def store_from_df(self, df):
        # bulk user is bad in sqlalchemy, as volumes are not big we can create a single query
        for _, row in df.iterrows():
            keys = {
                'exercise_id': row['exercise_id'],
                'user_id': row['user_id'],
                'timestamp': row['timestamp'],
            }
            data = {
                'sets': row['sets'],
                'reps': row['reps'],
                'weight': row['weight'],
            }
            self.update(obj, **data) if (obj := self.get(**keys)) else self.save(**keys, **data)

