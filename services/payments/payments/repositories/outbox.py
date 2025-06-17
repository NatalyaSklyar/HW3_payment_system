from collections.abc import Iterable

from sqlalchemy import delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from .base import PaymentOutboxEntry


class OutboxRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_entries(self, entries: list[PaymentOutboxEntry]) -> None:
        self.session.add_all(entries)

    async def add_entry(self, entry: PaymentOutboxEntry) -> None:
        self.session.add(entry)
