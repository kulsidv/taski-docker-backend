import os
import redis

from .utils import get_redis_connection_config


class CacheManager:
    DEFAULT_TTL = int(os.getenv("DEFAULT_CACHE_TTL", str(60 * 60 * 24)))

    def __init__(self):
        self.r = redis.Redis(**get_redis_connection_config())

    def get_data(self, key: str):
        return self.r.json().get(key)

    def exists(self, key: str):
        return self.r.exists(key) == 1

    def set_data(self, key: str, data: dict | list[dict], ttl: int = DEFAULT_TTL):
        is_exists = self.exists(key)
        if not is_exists:
            self.r.json().set(name=key, path="$", obj=data)
            self.r.expire(key, ttl)

    def delete_data(self, key: str):
        self.r.delete(key)


cache = CacheManager()
