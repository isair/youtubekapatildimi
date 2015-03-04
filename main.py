# -*- coding: utf-8 -*-

"""
main.py
Jan 14, 2014
Copyright (C) 2014 Baris Sencan
"""

import os
import redis
from flask import Flask, render_template, url_for
from flask.ext.compress import Compress

app = Flask(__name__)

# Enable gzip compression.
Compress(app)

# Static file loading helper.
app.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename=filename))

# Redis configuration.
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)

# DNS list (plot twist: it's actually a dictionary).
dns_list = {
    'Google': ('8.8.8.8', '8.8.4.4'),
    'OpenDNS': ('208.67.222.222', '208.67.220.220'),
    'TTNet': ('195.175.39.40', '195.175.39.39')
}

@app.route('/')
def home():
    # Fetch information from database and render page.
    status_for = dict()
    for server in dns_list:
        try:
            status_for[server] = redis.get(server)
        except:
            status_for[server] = 'unknown'
    return render_template('home.html', dns_list=dns_list, status_for=status_for)
