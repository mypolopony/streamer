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


def convert(seconds):
    '''
    Nicer time display
    '''
    return time.strftime("%H:%M:%S", time.gmtime(n))

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

# Location of local tweet database
tweetdb = 'tweetdb.json'

def open_db():
    # Local tweet database
    db = TinyDB(tweetdb)
    tweets = TinyDB.table(db, 'tweets')

    return tweets

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

def load_extant():
    '''
    Extant tweets are retrieved from manual download of account history from 
    Twitter. Unfortunately, the format needs to be pre-processed since Twitter
    produces invalid JSON. As long as this project remains in tact, it only needs
    to be done once, and it's not hard. This file is produced after that 
    transformation (it's just key-ifying the outer structure)

    This was actually excruciatingly slow, thanks tinydb :(
    '''

    # Tweet database
    tweets = open_db()

    with open('extant_jun_17_2020.json','r') as extant_in:
        extant = json.load(extant_in)
    extant = [e['tweet']['full_text'] for e in extant['data']]

    # 3525 tweets wow that's a lot. Confirmed by visiting Twitter, yikes. [June 17 2020]
    pprint('Found {} Existing Posts'.format(len(extant)))

    pprint('Creating Database / Table')
    try:
        for tweet in extant:
            tweets.insert({'text': tweet, 'posted': True})

    except Exception as e:
        pprint('Exception Encountered: {}'.format(e))
        os.remove(tweetdb)

    return


# Main things
if __name__ in ('__console__', '__main__'):

    pprint('Tervetuloa! Welcome!')

    # Using tinydb here, as it is perfect for these small projects. It's NoSQL
    # because I really hate SQL. I think it jus uses JSON for storage. . .

    '''
    # ONE TIMER-ISH
    # Initiate (this only needs to be done once). This will also load the extant
    # tweets
    if not os.path.exists(tweetdb):
        load_extant()

    # DO THIS OCCASIONALLY, manually add to TWEETME and then delete
    # Load those in the TWEETME queue
    if os.path.exists('TWEETME'):
        tweets = open_db()
    with open('TWEETME', 'r') as newtweets:
        for idx, line in enumerate(newtweets):
            tweets.insert({'text': line.replace('\n',''), 'posted': False})
    '''
    
    # Post loop
    while True:
        Tweet = Query()
        post = tweets.get(Tweet.posted == False)

        if post:
            _ = api.update_status(post['text'])
            pprint('Post Successful: {}'.format(post['text']))
            tweets.update({'posted':True}, doc_ids = [post.doc_id])

        # Wait 6 - 12 hours
        seconds = random.uniform(6,12) * 60 * 60
        pprint('Next update in {} hours'.format(round(seconds/60/60, 1)))
                
        time.sleep(seconds)
