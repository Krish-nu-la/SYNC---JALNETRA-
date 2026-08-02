import time


class CacheService:

    def __init__(self):

        self.cache = {}

        self.ttl = 300

    def get(self, key):

        if key not in self.cache:
            return None

        value, timestamp = self.cache[key]

        if time.time() - timestamp > self.ttl:

            del self.cache[key]

            return None

        return value

    def set(self, key, value):

        self.cache[key] = (
            value,
            time.time()
        )


cache_service = CacheService()