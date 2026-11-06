import os
from dotenv import load_dotenv
from redis import Redis
from rq import Queue

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

if REDIS_URL is None:
    raise RuntimeError("REDIS_URL is not set")

redis_connection = Redis.from_url(REDIS_URL)

judge_queue = Queue(
    "judge",
    connection=redis_connection
)