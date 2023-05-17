from .base import BaseEnum


class PayoutMethod(str, BaseEnum):

    CARD = 'card'
    CARD_UA = 'card_uah'
    CARD_FOREIGN = 'card_foreign'
    QIWI = 'qiwi'
    YOOMONEY = 'yoomoney'
    PAYEER = 'payeer'
    ADVCASH = 'advcash'
    PERFECTMONEY = 'perfect_money'
    WEBMONEY = 'webmoney'
    BITCOIN = 'bitcoin'
    LITECOIN = 'litecoin'
    USDT = 'tether'
    TRON = 'tron'
    DOGECOIN = 'dogecoin'
    ETHEREUM = 'ethereum'
    RIPPLE = 'ripple'
