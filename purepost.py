# -*- coding: utf-8 -*-
# @Author: Selwyn-Lloyd
# @Date:   2019-02-15 13:11:16
# @Last Modified by:   Selwyn-Lloyd McPherson
# @Last Modified time: 2020-10-31 23:10:55

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

# Location of local tweet database
# Using tinydb here, as it is perfect for these small projects. It's NoSQL
# because I really hate SQL. I think it jus uses JSON for storage. . .
tweetdb = 'tweetdb.json'

def convert(seconds):
    '''
    Nicer time display
    '''
    return time.strftime("%H:%M:%S", time.gmtime(n))

def open_db():
    # Local tweet database
    db = TinyDB(tweetdb)
    tweets = TinyDB.table(db, 'tweets')

    return tweets

def time_analysis():
    '''
    This is one of the most frustrating Pythonic experiences of all time.
    This method is not intended to be used functunally, but only for analysis and practice.

    We receive, from the main program, this. . . Keep in mind I use double quotes in-code
    and single quotes for comments. . . Just my style I guess. . .
    '''

    raw_data = """Sun Jul 19 07:03:55 2020: Next update in 15622.07397139018 seconds (4.3 hours)
    Sun Jul 19 11:24:18 2020: Next update in 15583.76668589194 seconds (4.3 hours)
    Mon Jul 20 00:43:29 2020: Next update in 13892.442895423877 seconds (3.9 hours)
    Mon Jul 20 05:00:53 2020: Next update in 17538.876418275577 seconds (4.9 hours)
    Mon Jul 20 13:16:15 2020: Next update in 12281.47739731487 seconds (3.4 hours)
    Mon Jul 20 16:41:13 2020: Next update in 20983.12822644447 seconds (5.8 hours)
    Mon Jul 20 22:30:57 2020: Next update in 14408.528000559105 seconds (4.0 hours)
    Tue Jul 21 05:14:16 2020: Next update in 18421.565193946757 seconds (5.1 hours)
    Tue Jul 21 13:21:41 2020: Next update in 19052.686349454507 seconds (5.3 hours)
    Tue Jul 21 18:39:15 2020: Next update in 20470.149045667447 seconds (5.7 hours)
    Wed Jul 22 00:20:26 2020: Next update in 17994.227905193908 seconds (5.0 hours)""".splitlines()

    '''
    The large discontinuities due to closing the app, restarting the computer, whatever, but
    it's easily parsible.

    At this point, we are archeologists, so let's not bother with actual coding practices
    '''

    # Sample line
    test_text = raw_data[0]

    # Sanity check on the text parsing
    try:
        # Re says
        import re
        pattern = re.compile('(?P<timestamp>.+): Next update in (?P<a>.+) seconds \((?P<hours>.+) hours\)') 
        re_result = re.search(pattern, text).groupdict()

        # parse says 
        import parse
        pattern = '{timestamp}: Next update in {seconds} seconds ({hours} hours)'
        p = parse.compile(pattern)
        parse_result = p.parse(text).named()

        # Are they the same? Dict comparison!
        assert(re_result == parse_result)

    except AssertionError:
        pprint('Sorry, your parser is broken [this shouldn\'t happen]')


    # Sanity check on the date parsing
    try:
        # Dateparser says
        import dateparser
        dt_dateparser = dateparser.parse(test_text)

        # Dateutil says
        from dateutil import parser
        dt_dateutil = parser.parse(test_text)

        # Datetime says #### UNFINISHED HERE
        from datetime import datetime, time
        dt_datetime = datetime.strptime('2015-01-01 01:00:00', '%Y-%m-%d %H:%M:%S')

        # What's the differene? Clearly nothing
        assert(dt_dateparser == dt_dateutil == dt_datetime)
    
    except AssertionError:
        pprint('Sorry, your date-time interpreter is broken [this shouldn\'t happen]')


    '''
    After all of that, we just have to pick one, I guess. Everything above was just flossing, the real
    question is: why do the time differences seem. . . different to me. . .
    '''

def console_input():
    '''
    Alternatives include:

    via: alias tweet='f(){ echo $1 >> ~/Projects/streamer/TWEETME }; f'
    via alias tweet='f(){ /usr/local/bin/python3 ~/Projects/streamer/purepost.py add'

    TODO: Tjos logic clearly needs to be changed
    '''

    # Check arguments
    if len(sys.argv) == 1 or sys.argv[1] not in ('add', 'run', 'status'):
        pprint('Use an argument: add or run')
        sys.exit(0)
    else:
        # Mode
        mode = sys.argv[1]

    if mode == 'add':
        post = '"' + ' '.join(sys.argv[2:]) + '"'

        db.queue.insert_one({'text': post})
        pprint('Added to Queue: {}'.format(post))

        sys.exit(0)
    elif mode == 'status':
        tweets = open_db()

        pprint('Posted: {}'.format(tweets.count(Tweet.posted == True)))
        pprint('Unpsted: {}'.format(tweets.count(Tweet.posted == False)))
        pprint('Remaining Unposted Time: {}'.)

        sys.exit(0)

def load_extant():
    '''
    [DEPRECATED]

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

    # 3525 tweets [as of June 17 2020] -- wow that's a lot. 
    pprint('Found {} Existing Posts'.format(len(extant)))

    pprint('Creating Database / Table')
    try:
        for tweet in extant:
            tweets.insert({'text': tweet, 'posted': True})

    except Exception as e:
        pprint('Exception Encountered: {}'.format(e))
        os.remove(tweetdb)

    return


if __name__ in ('__console__', '__main__'):
    # Say hello
    pprint('Tervetuloa! Welcome!')

    # Parse arguments
    console_input()

    # The queue, TWEETME, is just a flat file of current brilliant musings. It is of
    # some satisfaction to amass a respectable list before sending it to the *actual*
    # database queue, and a flat file one Command+Tab away is comforting to me. Nevertheless,
    # these (pre-)queues posts have to be scooped up at some point. Let's just have
    # the user decide whether she wants to do it now or defer.
    prequeue = 'TWEETME'
    if os.path.exists(prequeue):
        if input('TWEETME File Found. Send to DB? ("y" for yes): ') == 'y':
            tweets = open_db()
            with open(prequeue, 'r') as newtweets:
                for idx, line in enumerate(newtweets):
                    if '"' in line:
                        line = line.strip()
                        pprint((idx, line))
                        tweets.insert({'text': line, 'posted': False})

            pprint('{} tweets sent to local database'.format(idx + 1))       # Great idx + 1 here
            os.remove(prequeue)

    # Post loop
    while True:
        # Have to re-establish connection (it times out, which is less than ideal since
        # this will potentially run forever. . . -- we would ideally like to see if it's 
        # still open but. . . this is TinyDB for a reason. . .
        tweets = open_db()

        # A new tweet, if it exists
        Tweet = Query()
        post = tweets.get(Tweet.posted == False)

        if post:
            _ = api.update_status(post['text'])
            pprint('Post Successful: {}'.format(post['text']))
            tweets.update({'posted':True}, doc_ids = [post.doc_id])


        # Wait 3 - 6 hours
        seconds = random.uniform(3, 6) * 60 * 60
        pprint('Next update in {} seconds ({} hours)'.format(seconds, round(seconds/60/60, 1)))
                
        time.sleep(seconds)
