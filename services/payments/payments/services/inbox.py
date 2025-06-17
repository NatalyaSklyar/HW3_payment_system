import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from payments.repositories.accounts import AccountsRepository
from payments.repositories.inbox import InboxRepository, PaymentInboxEntry
from payments.repositories.outbox import OutboxRepository, PaymentOutboxEntry
from fastapi import HTTPException, status

from repositories.base import PaymentStatus


class InboxService:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self.sessionmaker = sessionmaker

    async def handle_withdraw(
        self,
        accounts_repo: AccountsRepository,
        entry: PaymentInboxEntry,
    ) -> PaymentStatus:
        db_account = await accounts_repo.get_account(entry.user_id)
        if db_account is None:
            return PaymentStatus.FAILED
        try:
            await accounts_repo.withdraw(entry.user_id, entry.amount, do_commit=False)
            return PaymentStatus.COMPLETED
        except ValueError as e:
            return PaymentStatus.CANCELLED

    async def inbox_daemon(self) -> None:
        while True:
            async with self.sessionmaker() as session:
                accounts_repo = AccountsRepository(session)
                inbox_repo = InboxRepository(session)
                outbox_repo = OutboxRepository(session)

                for entry in await inbox_repo.get_inbox_entries():
                    await inbox_repo.delete_entry(entry.id)
                    status = await self.handle_withdraw(accounts_repo, entry)
                    await outbox_repo.add_entry(
                        PaymentOutboxEntry(
                            id=entry.id,
                            status=status,
                        )
                    )
                    await session.commit()
            await asyncio.sleep(2)
