#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import credentials

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(credentials.key, credentials.secret)
    auth.set_access_token(credentials.authkey, credentials.authsecret)
    stream = Stream(auth, l)

    targets = ['fallujah', 'cats']
    stream.filter(track=targets)
