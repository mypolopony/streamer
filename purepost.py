# -*- coding: utf-8 -*-
# @Author: Selwyn-Lloyd
# @Date:   2019-02-15 13:11:16
# @Last Modified by:   Selwyn-Lloyd McPherson
# @Last Modified time: 2020-04-14 19:31:16

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
import credentials                      # Non-gitted credentials
from pymongo import MongoClient
from tweepy import OAuthHandler, API

def pprint(msg):
    '''
    Our own special pretty-print, because why not?
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

def announce();
    '''
    Just basic status check
    '''
    pass



def console_input():
    '''
    Add via command line (direct addition to the database)
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


def update_archives():
    '''
    Fortunately, or unfortunately, there are a number of sources based 
    on the constant evolution of this project. They are:
    '''

    '''
    1. Most recent (i.e. RAM) text file of intended posts and old raw text files 
        of intended posts
    '''

    txtsources = ['TWEETME', 'TWEETMEAGAIN']
    for txtsource in txtsources:
        with open(txtsource):
            db.queue.insert_one({'_id': post['_id']}, {'$set': {'posted': True}})

    '''
    2. Partial restorations of thousands of copy-paste history, captured
           by CopyClip, across two different versions, because I accidentally
           overwrote the above RAM and previous-RAM
            [these are exports from the raw CopyClip sqlite database; /db1 and /db2], 
                and yield JSONs
    ** This collection needs to be vetted, as not all copy-paste is a source

    '''

    # -- Input

    # -- Curation

    # -- Output / Registration

    


# Main things
if __name__ in ('__console__', '__main__'):
    pprint('Tervetuloa! Welcome!')

    while True:
        # Check for anything new and resolve the database
        update_archives()

        post = db.queue.find_one({'posted': False})
        if post:
            # Announce
            pprint('There\'s a new post!: {}'.format(post['text']))

            # Post
            api.update_status(post['text'])

            # Mark as posted
            db.queue.update_one({'_id': post['_id']}, {'$set': {'posted': True}})
            pprint('Posted: {}'.format(post['text']))
            

        # Wait for two hours +/- 60 minutes-ish, as if it weren't a bot
        seconds = 2 * 60 * 60 + 60 * random.randint(0, 60)
        pprint('Next update in {} minutes'.format(int(seconds / 60)))
                
        time.sleep(seconds)