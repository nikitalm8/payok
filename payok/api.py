import hashlib

from .models import (
    Transaction, 
    NewPayout,
    Payout, 
    Balance,
)
from .enums import (
    Currency,
    ComissionType,
    PaymentMethod,
    PayoutMethod,
)
from .exceptions import PayOKError

from urllib.parse import urlencode
from typing import Union, Optional, List

from aiohttp import ClientSession


class PayOK(object):
    """
    PayOK API Wrapper
    """

    API_URL = 'https://payok.io/api/%s'

    def __init__(
        self, 
        api_id: str, 
        api_key: str, 
        project_id: Optional[int]=None, 
        project_secret: Optional[str]=None,
        session: Optional[ClientSession]=None,
    ) -> None:
        """
        Initialize the wrapper

        :param str api_id: API ID
        :param str api_key: API Key
        :param Optional[int] project_id: Project ID, defaults to None
        :param Optional[str] project_secret: Project Secret, defaults to None
        :param Optional[ClientSession] session: AioHTTP client session
        """

        self.api_id = api_id
        self.api_key = api_key

        self.project_id = project_id
        self.project_secret = project_secret

        self.session = session or ClientSession()


    @staticmethod
    def _check_response(response: dict) -> None:
        """
        Check response for errors

        :param dict response: API response
        :raises PayOKError: Base API error
        """
        print(response)

        if response.get('status') == 'error':

            raise PayOKError(
                response['error_code'], 
                response.get('error_text') or response.get('text'),
            )


    async def _make_request(self, endpoint: str, **kwargs) -> dict:
        """
        Make a request to the API

        :param str endpoint: API Endpoint
        :return dict: API Response JSON
        """

        async with self.session.post(
            self.API_URL % endpoint,
            data={
                **{
                    key: value
                    for key, value in kwargs.items()
                    if value is not None
                }, 
                'API_ID': self.api_id,
                'API_KEY': self.api_key,
            },
        ) as response:

            data = await response.json(content_type=None)
            self._check_response(data)

            return data


    async def get_balance(self) -> Balance:
        """
        Get balance via API

        :return Balance: Balance model
        """

        result = await self._make_request('balance')
        return Balance(**result)


    async def get_transactions(self, payment_id: Optional[int]=None, offset: Optional[int]=None, project_id: Optional[int]=None) -> List[Transaction]:
        """
        Get all matching transactions via API

        :param Optional[int] payment_id: Filter by payment id
        :param Optional[int] offset: Offset for pagination
        :param Optional[int] project_id: Project id, if not set, will be used project id from __init__
        :return List[Transaction]: List of transactions (can be empty)
        """

        result = await self._make_request(
            'transaction',
            payment=payment_id,
            offset=offset,
            shop=project_id or self.project_id,
        )
        
        result.pop('status')
        return [
            Transaction(**transaction)
            for transaction in result.values()
        ]


    async def get_payouts(self, payout_id: Optional[int]=None, offset: Optional[int]=None) -> List[Payout]:
        """
        Get all matching payouts

        :param Optional[int] payout_id: Filter by payout id
        :param Optional[int] offset: Offset for pagination
        :return List[Payout]: List of payouts (can be empty)
        """

        result = await self._make_request(
            'payout',
            payout_id=payout_id,
            offset=offset,
        )

        result.pop('status')
        return [
            Payout(**payout)
            for payout in result.values()
        ]


    async def create_payout(
        self,
        amount: float,
        reciever: str,
        method: Union[PayoutMethod, str]=PayoutMethod.CARD,
        comission_type: Union[ComissionType, str]=ComissionType.BALANCE,
        webhook_url: Optional[str]=None,
    ) -> NewPayout:
        """
        Create a payout

        :param float amount: Payout amount
        :param str reciever: Reciever of payout
        :param str method: Payout method, defaults to "card"
        :param str comission_type: Where to take comission from, defaults to "balance"
        :param Optional[str] webhook_url: Webhook URL, defaults to None
        :return NewPayout: Payout model
        """

        result = await self._make_request(
            'payout_create',
            amount=amount,
            method=method,
            reciever=reciever,
            comission_type=comission_type,
            webhook_url=webhook_url,
        )
        return NewPayout(**result)


    async def create_bill(
        self, 
        pay_id: int,
        amount: Union[int, float],
        currency: Union[Currency, str]=Currency.RUB,
        description: str='Payment',
        method: Optional[Union[PaymentMethod, str]]=None,
        email: Optional[str]=None,
        success_url: Optional[str]=None,
        lang: Optional[str]=None,
        activate: bool=True,
        project_id: Optional[int]=None,
        project_secret: Optional[str]=None,
        **custom_params,
    ) -> str:
        """
        Construct a Bill URL

        :param int pay_id: Bill ID
        :param Union[int, float] amount: Bill amount
        :param str currency: Currency, defaults to "RUB"
        :param str description: Description, defaults to "Payment"
        :param Optional[str] method: Payment method, defaults to None
        :param Optional[str] email: Email, defaults to None
        :param Optional[str] success_url: Success URL, defaults to None
        :param Optional[str] lang: Language, defaults to None
        :param bool activate: Activate the bill by visiting the url
        :param Optional[int] project_id: Project id, defaults to one provided in __init__
        :param Optional[str] project_secret: Project secret, defaults to one provided in __init__
        :return str: Bill URL
        """

        sign_string = '|'.join(
            str(item) for item in
            [amount, pay_id, project_id or self.project_id, currency, description, project_secret or self.project_secret]
        )
        sign = hashlib.md5(sign_string.encode())

        params = {
            'amount': amount,
            'payment': pay_id,
            'shop': project_id or self.project_id,
            'currency': currency,
            'desc': description,
            'email': email,
            'success_url': success_url,
            'method': method,
            'lang': lang,
            'sign': sign.hexdigest(),
            'custom': custom_params or None,
        }
        url = 'https://payok.io/pay?' + urlencode(
            {
                key: value
                for key, value in params.items()
                if value is not None
            },
        )

        if activate:

            async with self.session.get(url):

                pass

        return url
