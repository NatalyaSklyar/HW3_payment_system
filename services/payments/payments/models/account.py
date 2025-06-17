from pydantic import BaseModel
from decimal import Decimal


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
