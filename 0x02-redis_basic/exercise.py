#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            value = fn(value)
        return value

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, fn=int)

    def call_history(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            input_key = method.__qualname__ + ":inputs"
            output_key = method.__qualname__ + ":outputs"

            self._redis.rpush(input_key, str(args))

            output = method(self, *args, **kwargs)

            self._redis.rpush(output_key, output)

            return output
        return wrapper

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def replay(method: Callable):
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        inputs = cache._redis.lrange(input_key, 0, -1)
        outputs = cache._redis.lrange(output_key, 0, -1)

        if not inputs or not outputs:
            print("No history found for this method.")
            return

        print(f"{method.__qualname__} was called {len(inputs)} times:")

        for inp, out in zip(inputs, outputs):
            inp = eval(inp.decode())
            out = out.decode()
            print(f"{method.__qualname__}(*{inp}) -> {out}")


# Example usage:
cache = Cache()
cache.store("foo")
cache.store("bar")
cache.store(42)
Cache.replay(cache.store)
