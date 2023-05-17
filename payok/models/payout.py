from ..enums import PayoutMethod, PayStatus

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, validator
from pydantic.fields import Field


class Payout(BaseModel):
    """
    Class for Payout model
    """

    payout_id: int = Field(..., alias='payout')
    method: PayoutMethod
    amount: float
    amount_profit: float
    comission_percent: float
    comission_fixed: float
    date_create: datetime = Field(..., alias='date')
    date_pay: Optional[datetime]
    status: PayStatus = Field(..., alias='payout_status_code')

    @validator('date_pay', 'date_create', pre=True)
    def validate_dates(date_str: str) -> Optional[datetime]:

        if not date_str:

            return

        return datetime.strptime(
            date_str,
            '%d.%m.%Y %H:%M:%S',
        )

    class Config:

        allow_population_by_field_name = True
