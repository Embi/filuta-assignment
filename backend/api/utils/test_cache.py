import asyncio
import json

import fakeredis
import pytest
from flexmock import flexmock

from api.utils import cache as redis


@pytest.mark.asyncio(scope="module")
async def test_cached_json_response(monkeypatch):
    fake_redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr("api.utils.cache.__REDIS", fake_redis)

    fake_response = {"some": "value"}

    @redis.cached_json_response(expire=100)
    async def foo(a: int, b: int):
        # Simulate some async workload
        await asyncio.sleep(0.1)
        return fake_response

    # First time get should return None and subsequently
    # set should be called
    flexmock(fake_redis).should_call("get").with_args("foo:42").once()
    flexmock(fake_redis).should_call("set").with_args(
        "foo:42", json.dumps(fake_response), ex=100
    ).once()

    value = await foo(42, 69)
    assert value == fake_response

    # Second time, value being already cached, get should return
    # the cached value and set should never be called
    flexmock(fake_redis).should_call("get").with_args("foo:42").once()
    flexmock(fake_redis).should_call("set").never()

    value = await foo(42, 69)
    assert value == fake_response


@pytest.mark.asyncio(scope="module")
async def test_cached_json_response_customkey(monkeypatch):
    # Test cutom key and args selection
    fake_redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr("api.utils.cache.__REDIS", fake_redis)

    fake_response = {"some": "value"}

    @redis.cached_json_response(custom_key="bar", key_args=[1, 0], expire=100)
    async def foo(a: int, b: int):
        # Simulate some async workload
        await asyncio.sleep(0.1)
        return fake_response

    flexmock(fake_redis).should_call("get").with_args("bar:69:42").once()
    flexmock(fake_redis).should_call("set").with_args(
        "bar:69:42", json.dumps(fake_response), ex=100
    ).once()

    value = await foo(42, 69)
    assert value == fake_response

    flexmock(fake_redis).should_call("get").with_args("bar:69:42").once()
    flexmock(fake_redis).should_call("set").never()

    value = await foo(42, 69)
    assert value == fake_response
