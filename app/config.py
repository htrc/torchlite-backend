"""Configuration.

There are lots of ways to do configuration; this is a work in
progress.  For the current iteration, see
https://stackoverflow.com/questions/73563804/what-is-the-recommended-way-to-instantiate-and-pass-around-a-redis-client-with-f

and

https://github.com/tegarimansyah/snippet/tree/main/python-fastapi/redis-connection


"""
import os
import redis
from dotenv import find_dotenv, load_dotenv


class TorchliteConfigError(Exception):
    """Torchlite error of some kind"""

    pass


if find_dotenv() is False:
    raise TorchliteConfigError("could not load .env file")

load_dotenv(find_dotenv())


def create_redis():
    return redis.ConnectionPool(
        host=os.getenv("DB_HOST", default="localhost"),
        port=os.getenv("DB_PORT", default=6379),
        db=os.getenv("DB_NUMBER", default=0),
        encoding="utf8",
        decode_responses=True,
    )


def get_db():
    persistence_db: redis.Redis = redis.Redis(connection_pool=persistence_db_pool)
    try:
        yield persistence_db
    finally:
        persistence_db.close()


persistence_db_pool = create_redis()
