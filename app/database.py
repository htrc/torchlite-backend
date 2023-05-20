# obsolete?

import redis

dev_pool = redis.ConnectionPool(host="localhost", port=6379, db=0)
dev_db = redis.Redis(connection_pool=dev_pool)

test_pool = redis.ConnectionPool(host="localhost", port=6379, db=1)
test_db = redis.Redis(connection_pool=test_pool)

prod_pool = redis.ConnectionPool(host="localhost", port=6379, db=2)
prod_db = redis.Redis(connection_pool=prod_pool)
