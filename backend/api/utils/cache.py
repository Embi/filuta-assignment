import json
from typing import List, Optional

import redis.asyncio as aioredis

# from core.utils.configuration import Configuration
from api.utils.conf import ApiSettings

__REDIS_URL = ApiSettings().redis_url
__REDIS = aioredis.from_url(__REDIS_URL, decode_responses=True)


def cached_json_response(
    custom_key: Optional[str] = None,
    key_args: List[int] = [0],
    expire: Optional[int] = None,
):
    """Decorator factory that creates a decorator for caching function JSON
    resutls in Redis. A custom key may be provided or the key is calculated
    from the function name and given function arguments. By default only the
    first argument is used for key calculation. It can be overriden by
    `key_args` param by specifying which args and in which order should be
    used.

    e.g.,
    @cached_json_response(key_args=[1,0], expire=100)
    async def foo(a: int, b: int):
        return 'some-value'

    will create key 'foo:{b}:{a}' with value 'some-value' in Redis that expires
    in 100 seconds.

    while @cached_json_response(expire=100) would produce key 'foo:{a}'

    and  @cached_json_response(custom_key='xx') would produce key 'xx:{a}'
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            key = custom_key
            if custom_key is None:
                key = f"{func.__name__}"
            for i in key_args:
                key += f":{args[i]}"
            response = await __REDIS.get(key)
            if response is None:
                response = await func(*args, **kwargs)
                await __REDIS.set(key, json.dumps(response), ex=expire)
            else:
                response = json.loads(response)
            return response

        return wrapper

    return decorator
