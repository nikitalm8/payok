from .base import BaseEnum


class ComissionType(str, BaseEnum):

    BALANCE = 'balance'
    PAYMENT = 'payment'
