from decimal import Decimal

from pydantic import BaseModel


class AccountResponse(BaseModel):
    user_id: int
    balance: Decimal


class CreateAccountRequest(BaseModel):
    user_id: int


class DepositRequest(BaseModel):
    user_id: int
    amount: Decimal


class WithdrawRequest(BaseModel):
    user_id: int
    amount: Decimal
