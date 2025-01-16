import time
from utils import logger


class SimpleExpiringDict:
    def __init__(self):
        self.store = {}

    def set(self, key, value, ttl):
        self.store[key] = (value, time.time() + ttl)
        logger.info(self.store)

    def get(self, key):
        logger.info(self.store)
        if key in self.store:
            value, expiry_time = self.store[key]
            if time.time() < expiry_time:
                return value
            else:
                del self.store[key]
        return None


cache = SimpleExpiringDict()
