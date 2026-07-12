from typing import Any


from config.config import Config
from extensions.cache import cache


def clear_trekker_open_treks_cache():
    """Delete cached GET /trekker/treks responses (base + all query filter variants)."""
    cache.delete(Config.TREKKER_OPEN_TREKS_KEY)

    try:
        redis_client = cache.cache._write_client
        patterns = (
            f"*{Config.TREKKER_OPEN_TREKS_KEY}*",
            "*trekker/treks*",
        ) # tuple of patterns to match
        seen = set() # set of keys that have been deleted
        for pattern in patterns:
            for key in redis_client.scan_iter(match=pattern):
                if key not in seen:
                    redis_client.delete(key) # delete the key
                    seen.add(key) # add the key to the set of keys that have been deleted as its already been deleted
    except Exception as e:
        print(f"Could not scan/delete trek cache keys: {e}")
