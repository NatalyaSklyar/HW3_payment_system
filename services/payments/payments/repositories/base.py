from datetime import datetime
from decimal import Decimal
import enum

from sqlalchemy import Numeric, func, UUID, VARCHAR
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from payments.config import Config


engine = create_async_engine(
    url=Config.DATABASE_URL,
)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    """
    Base class for all models.
    """


class Account(Base):
    __tablename__ = "accounts"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[int] = mapped_column(
        Numeric(precision=10, scale=2), nullable=False, default=Decimal("0.00")
    )


class PaymentInboxEntry(Base):
    __tablename__ = "payments_inbox"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2), nullable=False
    )


class PaymentStatus(str, enum.Enum):
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class PaymentOutboxEntry(Base):
    __tablename__ = "payments_outbox"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    status: Mapped[PaymentStatus] = mapped_column(VARCHAR(20))
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)


async def create_tables() -> None:
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
