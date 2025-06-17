from .base import Account
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from decimal import Decimal


class AccountsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_account(self, user_id: int) -> Account | None:
        return await self.session.get(Account, user_id)

    async def get_balance(self, user_id: int) -> Decimal:
        account = await self.session.get(Account, user_id)
        if account is None:
            raise ValueError("Account does not exist")
        return account.balance

    async def deposit(
        self,
        user_id: int,
        amount: Decimal,
        *,
        do_commit: bool = True,
    ) -> Account:
        account = await self.get_account(user_id)
        if account is None:
            raise ValueError("Account does not exist")

        account.balance += amount
        if do_commit:
            await self.session.commit()
        else:
            await self.session.flush()
        await self.session.refresh(account)
        return account

    async def withdraw(
        self,
        user_id: int,
        amount: Decimal,
        *,
        do_commit: bool = True,
    ) -> Account:
        await self.session.execute(
            text("SELECT pg_advisory_xact_lock(:lock_key)"), {"lock_key": user_id}
        )
        account = await self.get_account(user_id)
        if account is None:
            raise ValueError("Account does not exist")
        if account.balance < amount:
            raise ValueError("Insufficient balance")
        account.balance -= amount
        if do_commit:
            await self.session.commit()
        else:
            await self.session.flush()
        await self.session.refresh(account)
        return account

    async def create_account(self, user_id: int) -> Account:
        if await self.get_account(user_id) is not None:
            raise ValueError("Account already exists")

        new_account = Account(user_id=user_id, balance=Decimal("0.00"))
        self.session.add(new_account)
        await self.session.commit()
        await self.session.refresh(new_account)
        return new_account
