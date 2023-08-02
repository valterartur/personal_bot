from typing import List, Dict, Any


class BaseRepository:
    def __init__(self, model, session):
        self.session = session
        self.model = model

    def commit(self):
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def get(self, sort=None, **kwargs):
        query = self.session.query(self.model).filter_by(**kwargs)
        if sort is not None: 
            query = query.order_by(sort)
        return query.first()

    def save(self, **kwargs):
        record = self.model(**kwargs)
        self.session.add(record)
        return record

    def delete(self, **kwargs):
        return self.session.query(self.model).filter_by(**kwargs).delete()

    def update(self, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return instance

    def list(self):
        return self.session.query(self.model).all()

    def upsert(self, keys: List[str], data: Dict[str, Any]):
        instance = self.get(**{key: data[key] for key in keys})
        if instance:
            return self.update(instance, **data)
        else:
            return self.save(**data)


