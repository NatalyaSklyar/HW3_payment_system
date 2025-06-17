from typing import Annotated

from fastapi import Depends
from payments.repositories.base import Session
from payments.services.account import AccountService
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    return Session


SessionMakerDependency = Annotated[
    async_sessionmaker[AsyncSession], Depends(get_sessionmaker)
]


async def get_account_service(sessionmaker: SessionMakerDependency) -> AccountService:
    """
    Dependency to provide an instance of AccountService with the current session.
    """
    return AccountService(sessionmaker=sessionmaker)


AccountServiceDependency = Annotated[AccountService, Depends(get_account_service)]
