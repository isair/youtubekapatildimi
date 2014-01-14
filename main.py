# -*- coding: utf-8 -*-

"""
main.py
Jan 14, 2014
Copyright (C) 2014 Barış Şencan
"""

import os
import redis
import dns.resolver
from flask import Flask, render_template, url_for

app = Flask(__name__)

# Static file loading helper.
app.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename=filename))

# Redis configuration.
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)


@app.route('/')
def home():
    return render_template('home.html')
