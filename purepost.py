# -*- coding: utf-8 -*-
# @Author: Selwyn-Lloyd
# @Date:   2019-02-15 13:11:16
# @Last Modified by:   mypolopony
# @Last Modified time: 2020-02-05 20:18:41

'''
I often find turns of phrase that I think are pithy enough to etch 
them into the twitter machine. While consuming media, it is easy
to record these / copy and paste in a flat file, which I generally
always have open.

Wanting to post these brilliant finds, I use the Tweepy API to 
post them automatically at a reasonable pace,   
'''

import os
import sys
import time
import random
import datetime
import credentials          # Non-gitted credentials
from pymongo import MongoClient
from tweepy import OAuthHandler, API

def pprint(msg):
    '''
    Our own special pretty-print
    '''
    print('{}: {}'.format(datetime.datetime.now().strftime('%c'), msg))

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

def console_input():
    '''
    Add via command line (possible direct injection, but 
    not necessarily recommended)
    '''

    # Check arguments
    if len(sys.argv) == 1 or sys.argv[1] not in ('add', 'run'):
        pprint('Use an argument: add or run')
        sys.exit(0)
    else:
        # Mode
        mode = sys.argv[1]

    # Add via command line 
    if mode == 'add':
        post = '"' + ' '.join(sys.argv[2:]) + '"'

        db.queue.insert_one({'text': post})
        pprint('Added to Queue: {}'.format(post))

        sys.exit(0)


# Main things
if __name__ in ('__console__', '__main__'):
    pprint('Tervetuloa! Welcome!')

    # Populate queue using file (insensitive to redundancy)
    pprint('Checking TWEETME file for new entries')
    try:
        with open('TWEETME', 'r') as filequeue:
            for line in filequeue:
                if not db.queue.find_one({'text': line}):
                    db.queue.insert_one({'text': line, 'posted': False})
    except:
        # I think there may be a situation in which there is no file
        pass


    # Post loop
    while True:
        post = db.queue.find_one({'posted': False})
        if post:
            pprint('There\'s a new')
            api.update_status(post['text'])
            pprint('Posted: {}'.format(post['text']))
            db.queue.update_one({'_id': post['_id']}, {'$set': {'posted': True}})

        # Wait for two hours +/- 60 minutes, as if it weren't a bot
        seconds = 2 * 60 * 60 + 60 * random.randint(0, 60)
        pprint('Next update in {} minutes'.format(int(seconds / 60)))
                
        time.sleep(seconds)