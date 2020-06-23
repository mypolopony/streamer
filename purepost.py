# -*- coding: utf-8 -*-
# @Author: Selwyn-Lloyd
# @Date:   2019-02-15 13:11:16
# @Last Modified by:   Selwyn-Lloyd McPherson
# @Last Modified time: 2020-06-23 13:57:48

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
import json
import random
import argparse
import datetime
import credentials                      # Non-gitted credentials
from pymongo import MongoClient
from tinydb import TinyDB, Query
from tweepy import OAuthHandler, API


def pprint(msg):
    '''
    Our own special pretty-print
    '''
    print('{}: {}'.format(datetime.datetime.now().strftime('%c'), msg))


# Twitter authentication
auth = OAuthHandler(credentials.key, credentials.secret)
auth.set_access_token(credentials.authkey, credentials.authsecret)
pprint('Authenticated')

# Twitter / Tweepy API
api = API(auth)
pprint('API connected')

def console_input():
    '''
    # !!DEPRECATED!! 
    via: alias tweet='f(){ echo $1 >> ~/Projects/streamer/TWEETME }; f'

    # [not-yet] UN-DEPRECATED
    via alias tweet='f(){
        /usr/local/bin/python3 ~/Projects/streamer/purepost.py add'
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

def load_extant(tweetdb):
    '''
    Extant tweets are retrieved from manual download of account history from 
    Twitter. Unfortunately, the format needs to be pre-processed since Twitter
    produces invalid JSON. As long as this project remains in tact, it only needs
    to be done once, and it's not hard. This file is produced after that 
    transformation (it's just key-ifying the outer structure)

    This was actually excruciatingly slow, thanks tinydb :(
    '''

    with open('extant_jun_17_2020.json','r') as extant_in:
        extant = json.load(extant_in)
    extant = [e['tweet']['full_text'] for e in extant['data']]

    # 3525 tweets wow that's a lot. Confirmed by visiting Twitter, yikes. [June 17 2020]
    pprint('Found {} Existing Posts'.format(len(extant)))

    pprint('Creating Database')
    try:
        db = TinyDB(tweetdb)

        for tweet in extant:
            db.insert({'text': tweet, 'posted': True})

    except Exception as e:
        pprint('Exception Encountered: {}'.format(e))
        os.remove(tweetdb)

    return


# Main things
if __name__ in ('__console__', '__main__'):

    pprint('Tervetuloa! Welcome!')

    # Using tinydb here, as it is perfect for these small projects. It's NoSQL
    # because I really hate SQL. I think it jus uses JSON for storage. . .
    tweetdb = 'tweetdb.json'
    
    # Initiate (this only needs to be done once). Unfortunately, we can't just initiate
    # the database blindly, or it will create an empty one
    if not os.path.exists(tweetdb):
        load_extant(tweetdb)
    
    db = TinyDB(tweetdb)
    pprint('Database connection successful')
    
    # Post loop
    while True:
        Tweet = Query()
        post = db.get(Tweet.posted == False)
        if post:
            pprint('There\'s a new')
            api.update_status(post['text'])
            pprint('Posted: {}'.format(post['text']))
            db.queue.update_one({'_id': post['_id']}, {'$set': {'posted': True}})

        # Wait for two hours +/- 60 minutes, as if it weren't a bot
        seconds = 2 * 60 * 60 + 60 * random.randint(0, 60)
        pprint('Next update in {} minutes'.format(int(seconds / 60)))
                
        time.sleep(seconds)
