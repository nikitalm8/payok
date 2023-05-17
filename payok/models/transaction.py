import json

from ..enums import (
    Currency,
    PayStatus, 
    WebhookStatus, 
)

from datetime import datetime

from pydantic import BaseModel, validator
from pydantic.fields import Field


class Transaction(BaseModel):
    """
    Class for Transaction model
    """

    id: int = Field(..., alias='payment_id')
    email: str
    amount: float
    amount_profit: float 
    currency: Currency
    comission_percent: float
    comission_fixed: float
    method: str
    transaction: int
    date: datetime
    pay_date: datetime = None
    status: PayStatus = Field(PayStatus.waiting, alias='transaction_status')
    custom_fields: dict = {}
    webhook_status: WebhookStatus
    webhook_amount: int

    @property
    def is_paid(self) -> bool:

        return bool(self.status)

    @validator('custom_fields', pre=True)
    def validate_fields(raw_field: str) -> dict:

        string = raw_field.replace('&quot;', '\"')
        return json.loads(string)
