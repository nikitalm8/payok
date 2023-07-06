from pydantic import BaseModel


class Balance(BaseModel):
    """
    Model of balance
    """

    balance: float
    ref_balance: float
