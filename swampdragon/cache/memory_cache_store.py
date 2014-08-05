cache = {}


def store_data(data, key, ttl):
    cache[key] = data


def get_data(key):
    return cache[key]


def has_data(key):
    return cache.get(key) is not None


def remove(key):
    if has_data(key):
        cache.pop(key)
