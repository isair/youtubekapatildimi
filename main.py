import os
import redis
import dns.resolver
from flask import Flask

app = Flask(__name__)

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)


@app.route('/')
def home():
    return 'HAYIR'
