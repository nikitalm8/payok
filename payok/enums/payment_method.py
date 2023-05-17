from .base import BaseEnum


class PaymentMethod(str, BaseEnum):

    CARD = 'cd'
    QIWI = 'qw'
    YOOMONEY = 'ya'
    WEBMONEY = 'wm'
    PAYEER = 'pr'
    PERFECTMONEY = 'pm'
    ADVCASH = 'ad'
    MEGAFON = 'mg'
    BITCOIN = 'bt'
    USDT = 'th'
    LITECOIN = 'lt'
    DOGECOIN = 'dg'
