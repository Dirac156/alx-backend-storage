#!/usr/bin/env python3
"""
find by topic
"""


import pymongo


def log_stats(a: dict) -> int:
    """log"""
    connection = pymongo.MongoClient('mongodb://127.0.0.1:27017')
    logs = connection.logs.nginx
    return logs.count_documents(a)


if __name__ == "__main__":
    print(f"{log_stats({})} logs")
    print("Methods:")
    print(f"\tmethod GET: {log_stats({'method': 'GET'})}")
    print(f"\tmethod POST: {log_stats({'method': 'POST'})}")
    print(f"\tmethod PUT: {log_stats({'method': 'PUT'})}")
    print(f"\tmethod PATCH: {log_stats({'method': 'PATCH'})}")
    print(f"\tmethod DELETE: {log_stats({'method': 'DELETE'})}")
    print(f"{log_stats({'method': 'GET', 'path': '/status'})} status check")
