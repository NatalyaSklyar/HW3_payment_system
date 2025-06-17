from collections.abc import Iterable
from .base import PaymentOutboxEntry
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy import select, delete


class OutboxRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_entries(self, entries: list[PaymentOutboxEntry]) -> None:
        self.session.add_all(entries)

    async def add_entry(self, entry: PaymentOutboxEntry) -> None:
        self.session.add(entry)
