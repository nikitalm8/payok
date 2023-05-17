<div align="left">
    <h1>PayOK    <img src="https://payok.io/files/image/logo_white.svg" width=64 height=24></h1>
    <p align="left" >
        <a href="https://pypi.org/project/payok/">
            <img src="https://img.shields.io/pypi/v/payok.io?style=flat-square" alt="PyPI">
        </a>
        <a href="https://pypi.org/project/payok/">
            <img src="https://img.shields.io/pypi/dm/payok.io?style=flat-square" alt="PyPI">
        </a>
    </p>
</div>

A simple, yet powerful library for PayOK [API](https://payok.io/cabinet/documentation/doc_api_main)


## Usage

With ``PayOK`` you can easily create and retrieve payment and payout info, get informaition about your account's balance and commissions, etc.

## Documentation

Official docs can be found on the [API's webpage](https://payok.io/cabinet/documentation/doc_api_main)

## Installation

```bash
pip install payok.io
```

## Requirements

 - ``Python 3.7+``
 - ``aiohttp``
 - ``pydantic``

## Features

 - ``Asynchronous``
 - ``Exception handling``
 - ``Pydantic return model``
 - ``LightWeight``

## Basic example

```python
import payok

from payok import PayOK, PayOKError


api = PayOK(
    'api_id', 'api_key',
) 


async def main():

    try:

        await api.get_balance()

    except PayOKError as exc:

        print(exc)

    payments = await api.get_payments(project_id=1)  # project_id can be provided in __init__
    print(payments[0].id, payments[0].status)


asyncio.run(main())
```

Developed by Nikita Minaev (c) 2023
