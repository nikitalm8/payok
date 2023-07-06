from pydantic import BaseModel
from pydantic.fields import Field

from .payout import Payout


class NewPayout(BaseModel):

    remain_balance: float
    payout: Payout = Field(..., alias='data')
