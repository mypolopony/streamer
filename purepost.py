# -*- coding: utf-8 -*-
# @Author: Selwyn-Lloyd
# @Date:   2019-02-15 13:11:16
# @Last Modified by:   Selwyn-Lloyd McPherson
# @Last Modified time: 2020-04-17 01:59:22

'''
I often find turns of phrase that I think are pithy enough to etch 
into the twitter machine. While consuming media, it is easy to
record these / copy and paste in a flat file, which I generally
always have open.

Wanting to ------- these brilliant finds, I use the Tweepy API to 
post them automatically at a reasonable pace
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
        # Check for anything new and resolve / add to the database
        update_archives()

        posts = db.queue.find({'posted': False})

        # Announce
        pprint('There are {} unposted posts.'.format(posts.count()))

        if posts:
            '''
            Aha, there's something to do. A few options. Consider first
            that there should be no more than a few dozen valid, postable
            entries. So a method you would use for 20 million entries is 
            very different from one with 20.

            We just one one. A random one, because not only does order not
            matter, it's actually adventageous to shuffle the entries
        
            We've already determined that there is at least one unposted
            item, which is a nice signal. Unfortunately, we had to do a 
            broad query to determine that. It's okay, these things are pretty
            cheap, but in a larger system, you would either have to create
            an index on the 'posted' field, or set some other flag to 
            ensure that new items notify the overall system that there is a new
            item.

            I'm pretty sure db.queue.find() is at worst O(N) and at best O(1). If 
            you want to do db.queue.find()[0] that's definitely O(N). But that's
            a waste because we only want one for the moment.

            So requery with find_one seems okay but I'm not sure it's random. It
            actually might very well be. . .

            But there is another option which I think is assured to be random:

                db.queue.aggregate([{ $sample: { size: 1 } }])


            Now, I don't actually know the mechanism behind this query, and the 
            'aggregate' makes me feel like it is in fact loading all of the items
            and then just. . . picking one. Which is not what we want. But, at 
            this point, let's just assume the MongoDB people know what they're doing.

            Maybe we should have used this call initially, but again it's cost / benefit. 
            At this point, I'm not sure we can avoid gathering the entire set at some point, 
            and it's so very not important for this use case and basically just academic.
            '''

            # Less than ideal because it's not obvious that there will be one, although we
            # know there well be, but as such there is no error checking
            post = db.queue.aggregate([{ $sample: { size: 1 } }])

            print('Posting new: {}'.format(post['text']))
            api.update_status(post['text'])

            # Mark as posted
            db.queue.update_one({'_id': post['_id']}, {'$set': {'posted': True}})
            pprint('Successful')

        # Wait for two hours +/- 60 minutes-ish, as if it weren't a bot
        seconds = 2 * 60 * 60 + 60 * random.randint(0, 60)
        pprint('Next update in {} minutes'.format(int(seconds / 60)))
                
        time.sleep(seconds)