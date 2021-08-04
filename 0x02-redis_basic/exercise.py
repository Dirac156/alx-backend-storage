#!/usr/bin/env python3
"""
create a connection with redis database
"""
import redis
from uuid import uuid4
from typing import Callable, Optional, Union
from functools import wraps


def call_history(method: callable) -> callable:
    """ memorize user actions"""
    method_key = method.__qualname__
    inputs = method_key + ':input'
    outputs = method_key + ':output'

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ function  wrapped """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper


def count_calls(method: callable) -> callable:
    """ count the number of time a function is called """
    method_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ function wrapped """
        self._redis.incr(method_key)
        return method(self, *args, **kwds)

    return wrapper


class Cache:
    """
    store informations
    """

    def __init__(self):
        """construct the instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store new data and return a new uuid"""
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ get the element and return the decoded version"""
        data = self._redis.get(key)
        if (fn is not None):
            return fn(data)
        return data

    def get_str(self, data: str) -> str:
        """ return the decoded byte in string """
        return data.decode('utf-8')

    def get_int(self, data: str) -> int:
        """ return the decoded byte in integer """
        return int(data)
