# -*- coding: utf-8 -*-

"""
update.py
Jan 14, 2014
Copyright (C) 2014 Barış Şencan
"""

import os
import redis
import dns.resolver
import urllib2
from main import dns_list

dns_resolver = dns.resolver.Resolver()

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)

for name_server in dns_list:
    dns_resolver.nameservers = dns_list[name_server]

    try:
        answers = dns_resolver.query('youtube.com')
    except:
        answers = None

    if not answers:
        try:
            redis.set(name_server, 'dns_down')
        except:
            pass
        print name_server, 'is down'
        continue

    address = 'http://' + str(answers[0])

    try:
        response = urllib2.urlopen(address)
    except:
        try:
            redis.set(name_server, 'down')
        except:
            pass
        print address, 'is down when accessed from', name_server
        continue

    for line in response:
        if 'mahkeme' in line.lower():
            try:
                redis.set(name_server, 'court_blocked')
            except:
                pass
            print address, 'seems to be blocked by court order when requested from', name_server
            break

    try:
        redis.set(name_server, 'up')
    except:
        pass
    print address, 'reachable from', name_server
