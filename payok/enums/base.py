from enum import Enum


class BaseEnum(Enum):
    """
    Overrides __str__ for enum items
    """

    def __str__(self) -> str:

        return str(self.value)
