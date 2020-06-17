#### Streamer

This Streamer is unfortunately named because it refers to several very different functions interacting with the Twitter API.

### Stream
Monitor recent tweets and identify the top N most recent tuples. This is useful for identifying trending topics. 


### Purestream
A very simple filter implementation to to monitor the twitter stream at-large for an arbitrary number of targets. This is useful for monitoring rapidly fluid situations, i.e. mass casualties, sports events, award shows, by keyword(s).


### Purepost
This is the most significant module. It is a personal Twitter account manager which sanitizes previous posts, queues future posts and maintains a local database of tweets.