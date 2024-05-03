#!/usr/bin/env python3
""" Cache module """
import redis
import uuid
from typing import Union, Callable


class Cache:
    """ Cache class """
    def __init__(self):
        """ Initialize cache """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store data in redis """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    
    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """ Get data from redis """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            value = fn(value)
            
    def get_str(self, key: str) -> Union[str, None]:
        """ Get string from redis """
        return self.get(key, fn=lambda x: x.decode('utf-8'))
    
    def get_int(self, key: str) -> Union[int, None]:
        """ Get int from redis """
        return self.get(key, fn=int)
