#### Streamer

Will monitor recent tweets and identify the top N most recent tuples. This is useful for identifying trending topics.

#### Purestream

A very simple filter implementation to to monitor the twitter stream at-large for an arbitrary number of targets. This is particularly useful for monitoring rapidly fluid situations, i.e. mass casualties, sports events, award shows, etc. . .

#### Purepost

Uses a simple MongoDB database to queue posts. Sometimes, you come up with too many ideas, but you'd like to throttle them. There is an `add` functionality to add posts to the queue, and a `run` capability to periodically emit those messages to Twitter.

#### An incident occurred

# Approximately 600 intended tweets cultivated over about 10 months were overwritten by this drivel\

# RIP TWEETME

# -------

Woah, my buddy Spammer Riskaay! I haven't heard from this dude in a minute.

(Almost literally true) -- Actually, it's Bernie Sanders and the siren call (yep) of  neo-millenial-post-yippie-cute-girl-frizzy-haired-grass-roots-granola-loving (why wouldn't you?)-I'm-kind-of-in-love-with-you

But not *that* much.

Who knew endless texts and phone calls, somewhere between awkard and threatening, could be yours for just a small payment of $7.

Ground roots af.

# -------

thxobama 

# -------

I actjually thought i went through screenshots to find the rare capture of the text file from before but either that was a dream or I've entirely forgotten where it is. . . 


#### TODO:
- The list of stop-words is decent but should be adapted to the Twitterspace

- I would prefer a moving window, which would be much more representative of current events without giving too much due to historical events

- It would be easy to have a keypress to refresh the history

- Make it prettier!