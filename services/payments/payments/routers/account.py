from fastapi import APIRouter, Depends
from payments.dependencies import AccountServiceDependency
from payments.models.account import (
    AccountResponse,
    CreateAccountRequest,
    DepositRequest,
    WithdrawRequest,
)

router = APIRouter(
    tags=["Account"],
)


@router.get("/account/{user_id}", response_model=AccountResponse)
async def get_account(user_id: int, account_service: AccountServiceDependency):
    """
    Get account details for a given user ID.
    """
    return await account_service.get_account(user_id)


@router.post("/account", response_model=AccountResponse)
async def create_account(
    request: CreateAccountRequest, account_service: AccountServiceDependency
):
    """
    Create a new account for a user.
    """
    return await account_service.create_account(request)


@router.post("/account/deposit", response_model=AccountResponse)
async def deposit(request: DepositRequest, account_service: AccountServiceDependency):
    """
    Deposit an amount into the user's account.
    """
    return await account_service.deposit(request)


@router.post("/account/withdraw", response_model=AccountResponse)
async def withdraw(request: WithdrawRequest, account_service: AccountServiceDependency):
    """
    Withdraw an amount from the user's account.
    """
    return await account_service.withdraw(request)
