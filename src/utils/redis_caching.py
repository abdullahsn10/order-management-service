import redis
from src.settings.settings import REDIS

cache = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"], db=REDIS["DB"])


def set_cache(key: str, value: str, expire: int) -> None:
    """
    Set a key-value pair in the cache with an expiration time
    *Args:
        key (str): The key to set in the cache
        value (str): The value to set in the cache
        expire (int): The expiration time in seconds
    *Returns:
        None
    """
    cache.set(key, value, ex=expire)


def get_cache(key: str) -> str:
    """
    Get the value of a key from the cache
    *Args:
        key (str): The key to get from the cache
    *Returns:
        str: The value of the key
    """
    return cache.get(key)
