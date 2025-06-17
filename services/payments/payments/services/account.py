from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from payments.models.account import (
    AccountResponse,
    WithdrawRequest,
    DepositRequest,
    CreateAccountRequest,
)
from payments.repositories.accounts import AccountsRepository
from fastapi import HTTPException, status


class AccountService:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self.sessionmaker = sessionmaker

    async def create_account(self, request: CreateAccountRequest) -> AccountResponse:
        async with self.sessionmaker() as session:
            storage = AccountsRepository(session)

            db_account = await storage.get_account(request.user_id)
            if db_account is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Account already exists",
                )

            db_account = await storage.create_account(request.user_id)
            return AccountResponse(
                user_id=db_account.user_id,
                balance=db_account.balance,
            )

    async def get_account(self, user_id: int) -> AccountResponse:
        async with self.sessionmaker() as session:
            storage = AccountsRepository(session)

            db_account = await storage.get_account(user_id)
            if db_account is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Account not found",
                )
            return AccountResponse(
                user_id=db_account.user_id,
                balance=db_account.balance,
            )

    async def withdraw(self, request: WithdrawRequest) -> AccountResponse:
        async with self.sessionmaker() as session:
            storage = AccountsRepository(session)

            db_account = await storage.get_account(request.user_id)
            if db_account is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Account not found",
                )
            if db_account.balance < request.amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient balance",
                )
            try:
                db_account = await storage.withdraw(request.user_id, request.amount)
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e),
                )
            return AccountResponse(
                user_id=db_account.user_id,
                balance=db_account.balance,
            )

    async def deposit(self, request: DepositRequest) -> AccountResponse:
        async with self.sessionmaker() as session:
            storage = AccountsRepository(session)

            db_account = await storage.get_account(request.user_id)
            if db_account is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Account not found",
                )
            try:
                db_account = await storage.deposit(request.user_id, request.amount)
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e),
                )
            return AccountResponse(
                user_id=db_account.user_id,
                balance=db_account.balance,
            )
