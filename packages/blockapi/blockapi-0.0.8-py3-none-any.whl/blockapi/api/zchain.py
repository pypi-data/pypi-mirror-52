from blockapi.services import (
    BlockchainAPI,
    set_default_args_values,
    APIError,
    AddressNotExist,
    BadGateway,
    GatewayTimeOut,
    InternalServerError
    )
import pytz
from datetime import datetime

class ZchainAPI(BlockchainAPI):
    """
    coins: zcash
    API docs: https://explorer.zcha.in/api
    Explorer: https://explorer.zcha.in/
    """

    active = True

    currency_id = 'zcash'
    currency_ticker = 'zec'
    base_url = 'https://api.zcha.in'
    rate_limit = 0
    coef = 1
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'get_balance': '/v2/mainnet/accounts/{address}',
    }

    def get_balance(self):
        response = self.request('get_balance',
                                address=self.address)
        if not response:
            return 0

        return response.get('balance') * self.coef

