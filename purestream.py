# -*- coding: utf-8 -*-
# @Author: Selwyn-Lloyd
# @Date:   2019-02-15 13:11:16
# @Last Modified by:   Selwyn-Lloyd
# @Last Modified time: 2019-02-15 13:38:40

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys
from textwrap import TextWrapper

# Personal credentials
import credentials

#This is a basic listener received relevant tweets
class StdOutListener(StreamListener):

    def on_status(self, status):
        try:
            if 'RT' not in status.text:     # Don't duplicate
                cleantext = status.text.replace('\n','')
                print('{}\t{}\t{}\t{}'.format(status.author.screen_name, status.created_at, status.source, cleantext))
        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print('Error: {}'.format(status_code))
        return True

    def on_timeout(self):
        print('Timeout reached')


def main(targets):
    # Authentication to Twitter Streaming API
    auth = OAuthHandler(credentials.key, credentials.secret)
    auth.set_access_token(credentials.authkey, credentials.authsecret)

    # The strean
    stream = Stream(auth, StdOutListener())
    stream.filter(None, targets)


if __name__ in ('__console__', '__main__'):
    # Take arguments as targets
    targets = sys.argv[1:].split()

    if not targets:
        print('Use a space separated set of arguments to specify targets')
    else:
        print('Targets: {}'.format(targets))
        main(targets)