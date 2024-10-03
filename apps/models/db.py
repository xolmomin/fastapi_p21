from datetime import datetime

from sqlalchemy import delete as sqlalchemy_delete, Column, DateTime, update as sqlalchemy_update, create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import conf


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower() + 's'


class DatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self):
        self._engine = create_engine(conf.db.db_url)
        self._session = sessionmaker(self._engine, expire_on_commit=False)

    def create_all(self):
        with self._engine.begin() as conn:
            Base.metadata.create_all(conn)

    def drop_all(self):
        with self._engine.begin() as conn:
            Base.metadata.drop_all(conn)


db = DatabaseSession()
db.init()


# ----------------------------- ABSTRACTS ----------------------------------
class AbstractClass:
    @staticmethod
    def commit():
        try:
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()

    @classmethod
    def create(cls, **kwargs):  # Create
        object_ = cls(**kwargs)
        db.add(object_)
        cls.commit()
        return object_

    @classmethod
    def update(cls, id_, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id_)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        db.execute(query)
        cls.commit()

    @classmethod
    def get(cls, id_):
        query = select(cls).where(cls.id == id_)
        return (db.execute(query)).scalar()

    @classmethod
    def delete(cls, id_):
        query = sqlalchemy_delete(cls).where(cls.id == id_)
        db.execute(query)
        cls.commit()

    @classmethod
    def get_all(cls):
        return (db.execute(select(cls))).scalars()


class CreatedModel(Base, AbstractClass):
    __abstract__ = True
    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
