from sqlalchemy import BigInteger, func, DateTime, PickleType
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, sessionmaker
from sqlalchemy import JSON


class Base(AsyncAttrs, DeclarativeBase):
    # created:Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    # updated:Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    ...


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    model_gpt: Mapped[str] = mapped_column(default="gpt3")
    chatgpt_dialogue_history: Mapped[PickleType] = mapped_column(PickleType, nullable=True)
    yandexgpt_dialogue_history: Mapped[PickleType] = mapped_column(PickleType, nullable=True)
