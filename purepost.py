#!/usr/local/opt/python/bin/python3.7

# -*- coding: utf-8 -*-
# @Author: Selwyn-Lloyd
# @Date:   2019-02-15 13:11:16
# @Last Modified by:   Selwyn-Lloyd
# @Last Modified time: 2019-02-24 17:43:47

import os
import sys
import time
import random
import datetime
import credentials          # Non-gitted credentials
from pymongo import MongoClient
from tweepy import OAuthHandler, API

def pprint(msg):
    print('{}: {}'.format(datetime.datetime.now().strftime('%c'), msg))

if __name__ in ('__console__', '__main__'):
    # Check arguments
    if len(sys.argv) == 1 or sys.argv[1] not in ('add', 'run'):
        pprint('Use an argument: add or run')
        sys.exit(0)
    else:
        # Mode
        mode = sys.argv[1]

    # Database connection
    c = MongoClient()
    db = c['streamer']
    pprint('Database connection successful')

    # Twitter authentication
    auth = OAuthHandler(credentials.key, credentials.secret)
    auth.set_access_token(credentials.authkey, credentials.authsecret)
    pprint('Authenticated')

    # Twitter / Tweepy API
    api = API(auth)
    pprint('API connected')

    # Add
    if mode == 'add':
        post = '"' + ' '.join(sys.argv[2:]) + '"'

        db.queue.insert_one({'text': post})
        pprint('Added to Queue: {}'.format(post))

        sys.exit(0)

    # Monitor
    elif mode == 'run':
        pprint('Running. . .')

        while True:
            post = db.queue.find_one()
            if post:
                api.update_status(post['text'])
                pprint('Posted: {}'.format(post['text']))
                db.queue.delete_one({'_id': post['_id']})

            # Two hours +/- 60 minutes
            seconds = 2 * 60 * 60 + 60 * random.randint(0, 60)
            pprint('Next update in {} minutes'.format(int(seconds / 60)))
                    
            time.sleep(seconds)