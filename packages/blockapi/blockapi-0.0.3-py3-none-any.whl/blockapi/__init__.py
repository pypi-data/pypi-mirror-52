import random
from .services import BlockchainAPI,APIError,BadGateway,GatewayTimeOut,AddressNotExist,InternalServerError
import blockapi.api
import inspect

from .test import test_addresses

def get_random_api_class_for_coin(currency_id, exclude=[]):
    api_classes = get_api_classes_for_coin(currency_id)
    api_classes = [cl for cl in api_classes if not (cl in exclude)]
    return random.choice(api_classes) if api_classes else None

def get_api_classes_for_coin(currency_id):
    return [i for i in get_active_api_classes() if
            i.currency_id and
            i.currency_id == currency_id]

def get_all_supported_coins():
    return list(set(c.currency_id for c in get_active_api_classes()
           if c.currency_id))

def get_active_api_classes():
    #inheritors = _inheritors(BlockchainAPI)
    inheritors = _get_all_inheritors()
    return [i for i in inheritors if i.active]


def _inheritors(klass):
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses

def _get_subclasses(class_name):
    return [getattr(class_name,x) for x in dir(class_name) if not x.startswith('__')]

def _get_all_inheritors():
    all_inheritors = []

    tridy = _get_subclasses(blockapi.api)

    for trida in tridy:
        tridy_sub = _get_subclasses(trida)
        for trida_sub in tridy_sub:
            if inspect.isclass(trida_sub):
                if blockapi.services.BlockchainAPI in trida_sub.__bases__:
                    all_inheritors.append(trida_sub)
                    grandchildren = _inheritors(trida_sub)
                    if len(grandchildren) > 0:
                        all_inheritors += _inheritors(trida_sub)

    return all_inheritors


def get_working_apis_for_coin(currency_id,debug=False):
    coin_classes = get_api_classes_for_coin(currency_id)

    if currency_id in test_addresses:
        if len(test_addresses[currency_id]) == 0:
            return ()
    else:
        return ()

    coin_address = test_addresses[currency_id][0]
    working_apis = []

    api_ok = True
    for api_class in coin_classes:
        api_inst = api_class(coin_address)
        exception_class = None
        exception_msg = None
        try:
            api_inst.get_balance()

        except Exception as e:
            exception_class = e.__class__.__name__
            exception_msg = str(e)
            api_ok = False

        if debug:
            working_apis.append((api_class,exception_class,exception_msg))
        else:
            if api_ok:
                working_apis.append(api_class)

    return tuple(working_apis)

def get_working_apis(debug=False):
    all_coins = get_all_supported_coins()
    ok_apis = {}

    for a_coin in all_coins:
        ok_apis[a_coin] = get_working_apis_for_coin(a_coin,debug=debug)

    return ok_apis
