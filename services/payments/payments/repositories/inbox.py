from collections.abc import Iterable
from .base import PaymentInboxEntry
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy import select, delete


class InboxRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_inbox_entries(self, limit: int = 100) -> Iterable[PaymentInboxEntry]:
        result = await self.session.execute(select(PaymentInboxEntry).limit(limit))

        return result.scalars().all()

    async def add_entries(self, entries: list[PaymentInboxEntry]) -> None:
        self.session.add_all(entries)
        await self.session.commit()

    async def delete_entry(self, entry_id: str) -> None:
        await self.session.execute(
            delete(PaymentInboxEntry).where(PaymentInboxEntry.id == entry_id)
        )
