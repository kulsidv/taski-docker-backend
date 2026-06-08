import os


def get_redis_connection_config() -> dict:
    return {
        "host": os.getenv("REDIS_HOST", "localhost"),
        "port": int(os.getenv("REDIS_PORT", "6379")),
        "db": int(os.getenv("REDIS_DB", "0")),
        "password": os.getenv("REDIS_PASSWORD", None),
        "username": os.getenv("REDIS_USERNAME", None),
    }
