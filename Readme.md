#### Streamer is. . .

A simple example of how to monitor a twitter stream and pick out progressively important trends.

It's not hard at all, and it can be interesting with the filter.  

## Twitter Sentiment Analusis
- remember to download nltk's vader_lexicon
- using development version (3/2/16) due to issues with vader


'''
Python 3.5.0 (default, Dec 10 2015, 17:10:39)
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from nltk.sentiment.vader import SentimentIntensityAnalyzer
>>> nltk.download()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'nltk' is not defined
>>> import nltk
>>> nltk.download()
showing info https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/index.xml
True
>>> sid = SentimentIntensityAnalyzer(
... )
>>> from nltk.sentiment.vader import SentimentIntensityAnalyzer
>>> sentence = "the twin towers collapsed today"
>>> ss = sid.polarity_scores(sentence)
>>> ss
{'compound': -0.2732, 'neu': 0.656, 'neg': 0.344, 'pos': 0.0}
>>> sid.polarity('I love rock and roll')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'SentimentIntensityAnalyzer' object has no attribute 'polarity'
>>> sid.polarity('I love rock and roll')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'SentimentIntensityAnalyzer' object has no attribute 'polarity'
>>> sid
<nltk.sentiment.vader.SentimentIntensityAnalyzer object at 0x10abd40b8>
>>> sid.polarity
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'SentimentIntensityAnalyzer' object has no attribute 'polarity'
>>> sid.polarity_scores(sentence)
{'compound': -0.2732, 'neu': 0.656, 'neg': 0.344, 'pos': 0.0}
>>> sid.polarity_scores('I absolutely love rock and roll')
{'compound': 0.6697, 'neu': 0.471, 'neg': 0.0, 'pos': 0.529}
>>> sentence = 'Should have asked Koppel where his fellow journalist were Re: Hillary and Bengazi.'
>>> sid.polarity_scores(sentence)
{'compound': 0.0, 'neu': 1.0, 'neg': 0.0, 'pos': 0.0}
>>> sentence = 'Should have done that'
>>> sid.polarity_scores(sentence)
{'compound': 0.0, 'neu': 1.0, 'neg': 0.0, 'pos': 0.0}
>>> sentence = 'Wouldn't Koppel just make up some shit?'
  File "<stdin>", line 1
    sentence = 'Wouldn't Koppel just make up some shit?'
                       ^
SyntaxError: invalid syntax
>>> sentence = "Wouldn't Koppel just make up some shit?"
>>> sid.polarity_scores(sentence)
{'compound': -0.5574, 'neu': 0.625, 'neg': 0.375, 'pos': 0.0}
>>> sentence = 'The nerve of Ted Koppel. '
>>> sid.polarity_scores(sentence)
{'compound': 0.0, 'neu': 1.0, 'neg': 0.0, 'pos': 0.0}
>>> invalid command name "exit"
    while executing
"exit"
'''
  

#### TODO:
The list of stop-words is decent but should be adapted to the Twitterspace. 

I would prefer a moving window, which would be much more representative of current events without giving too much due to historical events.

Make it prettier!