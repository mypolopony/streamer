# -*- coding: utf-8 -*-
# @Author: Selwyn-Lloyd
# @Date:   2019-02-15 13:11:16
# @Last Modified by:   Selwyn-Lloyd McPherson
# @Last Modified time: 2020-11-18 01:31:11

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pprint import pprint
import os
import sys
import json
import argparse
import credentials          # Non-gitted credentials

# Destination directory
dest_dir = 'library'
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# This is a basic listener received relevant tweets
# We extend it to take the output file
class StdOutListener(StreamListener):

    def __init__(self, targets, verbose = False):
        # This is the fun 'super' call required when overriding __init__
        super(StdOutListener, self).__init__()

        # Register targets and distination file
        self.targets = targets             # Not used class-wide, but useful
        self.outname = '_'.join(targets)   # Also not used class-wide but useful

        # I hate this construction because it opens a file without explicitly
        # closing it. Python does in fact do a good job with closing opened 
        # I/O things, and garbage collection, and all that, but it always seems
        # uneasy to me. . .
        self.outfile = open(os.path.join(dest_dir, self.outname), 'a')

        # Log level (to console)
        self.verbose = verbose

    def on_status(self, status):
        '''
        A message has been received
        '''
        try:
            if 'RT' not in status.text:     # Don't duplicate
                # Write to the appropriate file
                #
                # This is actually a lot of opening and closing; the alternative
                # would be to open the files during initialization, then refer
                # to them that way.
                try:
                    if self.verbose:
                        print('\n++ Status ++\n{}\n'.format(str(status)))
                    text = status.extended_tweet['full_text']
                except Exception as e:
                    text = status.text

                text = text.replace('\n', '').lower()

                print('{}\t{}'.format(status.created_at, text))

                self.outfile.write('{}\t{}\t{}\t{}\n'.format(
                        status.author.screen_name,
                        status.created_at,
                        status.source, 
                        text))

        except Exception as e:
            # Catch any unicode errors while printing to console
            # and just ignore them: quantity > quality in this case
            print(e)
            pass

    def on_error(self, status_code):
        '''
        Here is a fun thing to notice:

        If you try to run the streamer in two processes, you might get killed with a 420 error.

        This occurred because I was not certain about capitalization, and tried two 
        separate instantiations to compare the difference. Unfortunately, that overloaded
        the API and I was (likely temporarily) shut out. Makes sense!
        '''
        
        print('Error: {}'.format(status_code))
        return True

    def on_timeout(self):
        '''
        Timeout, likely loss of connection
        '''
        print('Timeout reached')


def main(args):
    # Authentication to Twitter Streaming API
    auth = OAuthHandler(credentials.key, credentials.secret)
    auth.set_access_token(credentials.authkey, credentials.authsecret)

    # The stream
    stream = Stream(auth, StdOutListener(args.targets, args.verbose))
    stream.filter(None, args.targets)


if __name__ in ('__console__', '__main__'):
    # Handle arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('targets', type=str, nargs='*',
                        help='Search terms, quotes respected')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Debug mode / increase output verbosity')
    args = parser.parse_args()

    # Targets
    print('Targets: {}'.format(args.targets))

    # Run
    if args.verbose:
        print('Verbose Mode: ON')

    main(args)