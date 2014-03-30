connection_pool = []


def add_connection(connection):
    if connection not in connection_pool:
        connection_pool.append(connection)


def get_connection(uid=None):
    return connection_pool[-1]
