from .payout import Payout

from pydantic import BaseModel
from pydantic.fields import Field


class NewPayout(BaseModel):

    remain_balance: float
    payout: Payout = Field(..., alias='data')
