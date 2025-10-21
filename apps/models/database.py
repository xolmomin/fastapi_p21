from datetime import datetime
from venv import create

from faker import Faker
from sqlalchemy import BigInteger, delete as sqlalchemy_delete, DateTime, update as sqlalchemy_update, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, selectinload

from config import conf


class Base(AsyncAttrs, DeclarativeBase):

    @declared_attr
    def __tablename__(self) -> str:
        __name = self.__name__[:1]
        for i in self.__name__[1:]:
            if i.isupper():
                __name += '_'
            __name += i
        __name = __name.lower()

        if __name.endswith('y'):
            __name = __name[:-1] + 'ie'
        return __name + 's'


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self):
        self._engine = create_async_engine(conf.db.db_url)
        self._session = sessionmaker(self._engine, class_=AsyncSession)()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


db = AsyncDatabaseSession()
db.init()


# ----------------------------- ABSTRACTS ----------------------------------
class AbstractClass:
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception as e:
            print(e)
            await db.rollback()

    @classmethod
    async def create(cls, **kwargs):  # Create
        object_ = cls(**kwargs)
        db.add(object_)
        await cls.commit()
        return object_

    @classmethod
    async def update(cls, id_, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id_)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def get(cls, criteria, *, relationship=None):
        query = select(cls).where(criteria)
        if relationship:
            query = query.options(selectinload(relationship))
        return (await db.execute(query)).scalar()

    @classmethod
    async def count(cls):
        query = select(func.count()).select_from(cls)
        return (await db.execute(query)).scalar()

    @classmethod
    async def generate(cls, count: int = 1):
        return Faker()

    @classmethod
    async def delete(cls, id_):
        query = sqlalchemy_delete(cls).where(cls.id == id_)
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def filter(
            cls,
            *criteria,
            relationship=None,
            columns=None,
            use_or=False,
            **filters,
    ):
        """
        #
        # # 1️⃣ Oddiy filter (AND)
        # users = await User.filter(name="Ali", age=25)
        #
        # # 2️⃣ Bitta criterion bilan
        # users = await User.filter(User.email.like('%@gmail.com'))
        #
        # # 3️⃣ Bir nechta criterion OR bilan
        # users = await User.filter(User.age < 18, User.role == "student", use_or=True)
        #
        # # 4️⃣ Faqat ma’lum ustunlarni tanlash
        # names = await User.filter(age=25, columns=[User.name])
        #
        # # 5️⃣ Relationshipni preload qilish
        # users = await User.filter(User.is_active == True, relationship="profile")

        Universal filter for flexible querying.
        Examples:
            await User.filter(name="Ali", age=20)
            await User.filter(User.age > 18, User.name.like('%a%'))
            await User.filter(User.role.in_(['admin', 'editor']), use_or=True)
        """
        if columns:
            query = select(*columns)
        else:
            query = select(cls)

        # Add dynamic filters (**kwargs)
        if filters:
            dynamic_filters = [getattr(cls, k) == v for k, v in filters.items()]
            criteria = (*criteria, *dynamic_filters)

        if criteria:
            query = query.where(or_(*criteria) if use_or else and_(*criteria))

        if relationship:
            query = query.options(selectinload(relationship))

        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def all(cls):
        return (await db.execute(select(cls))).scalars()


class BaseModel(Base, AbstractClass):
    __abstract__ = True
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    def __str__(self):
        return f"{self.id}"


class CreatedBaseModel(BaseModel):
    __abstract__ = True
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
