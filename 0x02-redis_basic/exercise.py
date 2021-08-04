#!/usr/bin/env python3
"""
create a connection with redis database
"""
import redis
from uuid import uuid4
from typing import Union


class Cache:
    """
    store informations
    """

    def __init__(self):
        """construct the instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store new data and return a new uuid"""
        key = str(uuid4())
        self._redis.mset({key: data})
        return key
