#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import credentials
import json
from Queue import Queue
from threading import Thread
import time
from skimage import io
import os
# import cv2
import numpy
import sys

# Save haven for wayward global variables
imagequeue = Queue()
# ---------------------------------------
'''
def show_image(q):
  while True:
    data = q.get()

    # sci-kit show image
    print('THREAD 1 : START')
    img = io.imread(data['media'])
    cv2.imshow('image',img)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()

    q.task_done()


# Worker is going to continually process (show) images
worker = Thread(target=show_image, args=(imagequeue,))
worker.setDaemon(False)
worker.start()
'''

# 
# Need this instead: http://www.rediscookbook.org/implement_a_fifo_queue.html
#

#This is a basic listener received relevant tweets
class StdOutListener(StreamListener):

    def on_data(self, data):
        try: 
            # Data is {u'contributors': None, u'truncated': False, u'text': u'RT @BillFOX46: Chief Putney just announced that officers were looking for a wanted suspect, but saw Keith Scott w/ weed, then he drew a gun\u2026', u'is_quote_status': False, u'in_reply_to_status_id': None, u'id': 779801599250145280, u'favorite_count': 0, u'source': u'<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', u'retweeted': False, u'coordinates': None, u'timestamp_ms': u'1474754163931', u'entities': {u'user_mentions': [{u'id': 1071585991, u'indices': [3, 13], u'id_str': u'1071585991', u'screen_name': u'BillFOX46', u'name': u'Bill Melugin'}], u'symbols': [], u'hashtags': [], u'urls': []}, u'in_reply_to_screen_name': None, u'id_str': u'779801599250145280', u'retweet_count': 0, u'in_reply_to_user_id': None, u'favorited': False, u'retweeted_status': {u'contributors': None, u'truncated': False, u'text': u'Chief Putney just announced that officers were looking for a wanted suspect, but saw Keith Scott w/ weed, then he drew a gun, escalated.', u'is_quote_status': False, u'in_reply_to_status_id': None, u'id': 779784560812908545, u'favorite_count': 44, u'source': u'<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', u'retweeted': False, u'coordinates': None, u'entities': {u'user_mentions': [], u'symbols': [], u'hashtags': [], u'urls': []}, u'in_reply_to_screen_name': None, u'id_str': u'779784560812908545', u'retweet_count': 74, u'in_reply_to_user_id': None, u'favorited': False, u'user': {u'follow_request_sent': None, u'profile_use_background_image': False, u'default_profile_image': False, u'id': 1071585991, u'verified': True, u'profile_image_url_https': u'https://pbs.twimg.com/profile_images/768583642272661504/SoZT-32j_normal.jpg', u'profile_sidebar_fill_color': u'DDEEF6', u'profile_text_color': u'333333', u'followers_count': 1952, u'profile_sidebar_border_color': u'FFFFFF', u'id_str': u'1071585991', u'profile_background_color': u'C0DEED', u'listed_count': 70, u'profile_background_image_url_https': u'https://pbs.twimg.com/profile_background_images/431941969468612608/Q2MWZulT.jpeg', u'utc_offset': -14400, u'statuses_count': 3466, u'description': u'Anchor/reporter for WJZY-TV (FOX O&O) in Charlotte, NC. Proud ASU Cronkite school grad. Story idea? Would love to hear from you!William.Melugin@foxtv.com', u'friends_count': 622, u'location': None, u'profile_link_color': u'0084B4', u'profile_image_url': u'http://pbs.twimg.com/profile_images/768583642272661504/SoZT-32j_normal.jpg', u'following': None, u'geo_enabled': False, u'profile_banner_url': u'https://pbs.twimg.com/profile_banners/1071585991/1453928187', u'profile_background_image_url': u'http://pbs.twimg.com/profile_background_images/431941969468612608/Q2MWZulT.jpeg', u'name': u'Bill Melugin', u'lang': u'en', u'profile_background_tile': False, u'favourites_count': 452, u'screen_name': u'BillFOX46', u'notifications': None, u'url': None, u'created_at': u'Tue Jan 08 18:03:50 +0000 2013', u'contributors_enabled': False, u'time_zone': u'Eastern Time (US & Canada)', u'protected': False, u'default_profile': False, u'is_translator': False}, u'geo': None, u'in_reply_to_user_id_str': None, u'lang': u'en', u'created_at': u'Sat Sep 24 20:48:21 +0000 2016', u'filter_level': u'low', u'in_reply_to_status_id_str': None, u'place': None}, u'user': {u'follow_request_sent': None, u'profile_use_background_image': True, u'default_profile_image': False, u'id': 50216791, u'verified': False, u'profile_image_url_https': u'https://pbs.twimg.com/profile_images/778102542521819136/tk_QyqOK_normal.jpg', u'profile_sidebar_fill_color': u'C7CCCF', u'profile_text_color': u'E045E0', u'followers_count': 375, u'profile_sidebar_border_color': u'000000', u'id_str': u'50216791', u'profile_background_color': u'B6D1DE', u'listed_count': 2, u'profile_background_image_url_https': u'https://pbs.twimg.com/profile_background_images/837958963/7df56045b244bbf07d5e437115b14b8e.jpeg', u'utc_offset': -18000, u'statuses_count': 19484, u'description': u'00110011 00110110 00110101', u'friends_count': 268, u'location': None, u'profile_link_color': u'E045E0', u'profile_image_url': u'http://pbs.twimg.com/profile_images/778102542521819136/tk_QyqOK_normal.jpg', u'following': None, u'geo_enabled': True, u'profile_banner_url': u'https://pbs.twimg.com/profile_banners/50216791/1474349078', u'profile_background_image_url': u'http://pbs.twimg.com/profile_background_images/837958963/7df56045b244bbf07d5e437115b14b8e.jpeg', u'name': u'Wiley', u'lang': u'en', u'profile_background_tile': True, u'favourites_count': 4575, u'screen_name': u'KN12', u'notifications': None, u'url': None, u'created_at': u'Wed Jun 24 04:44:32 +0000 2009', u'contributors_enabled': False, u'time_zone': u'Central Time (US & Canada)', u'protected': False, u'default_profile': False, u'is_translator': False}, u'geo': None, u'in_reply_to_user_id_str': None, u'lang': u'en', u'created_at': u'Sat Sep 24 21:56:03 +0000 2016', u'filter_level': u'low', u'in_reply_to_status_id_str': None, u'place': None
            data = json.loads(data)
            timestamp = data['timestamp_ms']
            text = data['text'].encode('utf-8').replace('\n','')

            # Don't show retweets
            if 'RT' not in text and target in text:
                print('{} | {}'.format(timestamp,text))
            print('{} | {}'.format(timestamp,text))

            # print(json.dumps(data))
            # print('\n')
    
            if 'media' in data['entities'].keys():
                url = data['entities']['media'][0]['media_url']
                img = io.imread(url)

                
                # Unsurprisingly a poor idea:
                # cv2.imshow('image',img)
                # cv2.waitKey(1000)
                # cv2.destroyAllWindows()
        except Exception as e:
            pass
            # print('Skipping: {}'.format(e))

        return True


def on_error(self, status):
    # print(status)
    pass


def main(target):
    print(target)
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(credentials.key, credentials.secret)
    auth.set_access_token(credentials.authkey, credentials.authsecret)
    stream = Stream(auth, l)

    stream.filter(track=list(target))


if __name__ == '__main__':
    target = 'kellyanne'

    print('Target: {}'.format(target))
    main(target)
