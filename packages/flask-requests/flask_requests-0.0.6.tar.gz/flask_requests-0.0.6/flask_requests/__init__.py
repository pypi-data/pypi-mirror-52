from typing import Tuple, Any, Optional
from urllib.parse import urlparse

from blinker import Namespace
from flask import request

my_signals = Namespace()
parse_data = my_signals.signal('parse_data')


@parse_data.connect
def _parse_url_query(sender: str, *keys: str, **kwargs) -> Optional[Tuple]:
    if request.method == 'GET':
        parsed = urlparse(request.full_path)
        if parsed.query:
            parameter_iter = map(lambda x: x.split('='), parsed.query.split('&'))
            contained_keys = filter(lambda x: lambda x: len(x) == 2 and x[0] in keys, parameter_iter)
            return tuple(map(lambda x: x[1], contained_keys))
    return None


@parse_data.connect
def _parse_json(sender: str, *keys: str, **kwargs) -> Optional[Tuple]:
    if request.method == 'POST' and request.mimetype == 'application/json':
        return tuple(request.json.get(i, '') for i in keys)
    return None


@parse_data.connect
def _parse_form(sender: str, *keys: str, **kwargs) -> Optional[Tuple]:
    if request.method == 'POST' and request.mimetype == 'application/x-www-form-urlencoded':
        return tuple(request.json.get(i, '') for i in keys)
    return None


def get_data(*keys: str, data_source: request = request) -> Tuple[Any, ...]:
    """
    1. if mimetype is 'application/x-www-form-urlencoded', front end html example:
        action: request url
        name: name is necessary, name is ImmutableMultiDict item key
        <form role="form" action="/download-file/"
                  target="_self"
                  accept-charset="UTF-8"
                  method="POST"
                  autocomplete="off"
                  enctype="application/x-www-form-urlencoded">
            <textarea name="comment"></textarea>
            <input ..../>
        </form>

    2. support get data from url, such as http://0.0.0.0:8889/companies&token=xxxx
    get_data('token') -> 'xxxx'
    :return:
    """
    result = parse_data.send('parse_data', method=request.method, mimetype=request.mimetype, url=request.full_path)
    only_result = map(lambda x: x[1], result)
    valid_result = list(filter(lambda x: x is not None, only_result))
    if valid_result:
        return valid_result.pop()
    else:
        raise NotImplementedError(f'method {request.method}, mimetype {request.mimetype}, url {request.full_path}')


def get_token(token_key: str = 'token') -> str:
    """
    support get token from url/form and json
    :param token_key:
    :return:
    """
    return get_data(token_key)[0]
