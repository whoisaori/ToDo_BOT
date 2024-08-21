import os
from dotenv import load_dotenv
from datetime import datetime

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import (AsyncAttrs,
                                    create_async_engine,
                                    async_sessionmaker)
from sqlalchemy import ForeignKey, String


load_dotenv()
SQLALCHEMY_URL = os.getenv('SQLALCHEMY_URL')

engine = create_async_engine(SQLALCHEMY_URL, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True)


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger,
                                         ForeignKey('users.tg_id'),
                                         nullable=False)
    user = relationship('User', backref='tasks')
    title: Mapped[str] = mapped_column(String(50), nullable=False,)
    description: Mapped[str] = mapped_column(
        String(250),
        nullable=True,
        default=None
        )
    created_on: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=datetime.now)
    completion_time: Mapped[datetime] = mapped_column(
        nullable=True,
        default=None
        )


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
