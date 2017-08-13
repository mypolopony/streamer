import os
import re
import operator
import sys, getopt
from twython import TwythonStreamer
from textblob import TextBlob
from nltk.stem.lancaster import LancasterStemmer # I really don't like this stemmer but it's standard

# For security
import credentials

## As always, wayward home for lost but global variables (and functions!)
clear = lambda: os.system('clear')
st = LancasterStemmer()	# Not using this currently

class MyStreamer(TwythonStreamer):
	def staging(self):
		self.bookshelf = dict()
		self.count = 0
		self.stemmer = YasumasaStemmer()

		with open('stop_words.txt','r') as sw:
			self.stop_words = sw.read().splitlines()

	
	def on_success(self, data):
		# Digest
		if 'text' in data:
			line = data['text']
			
			# Do n-grams
			blob = TextBlob(line)
			ngrams = list(blob.ngrams(n=2))
			for ng in ngrams:
				for word in list(ng):
						word = word.lower()
						if word in self.stemmer.stems.keys():
								word = self.stemmer.stems[word]
						match = re.search('\w+',word)
						if match:
								word = match.group()
						if word in self.stop_words:
								word = ''
				if ng[0] and ng[1]:
						if ' '.join(ng) in self.bookshelf.keys():
								self.bookshelf[' '.join(ng)] += 1
						else:
								self.bookshelf[' '.join(ng)] = 1

			'''
			# Do Unigrams
			for word in line.split(' '):
				word = word.lower()

				# Stemming
				if word in self.stemmer.stems.keys():
					word = self.stemmer.stems[word]

				# Removing punctuation
				match = re.search('\w+',word)
				if match:
					word = match.group()

				# Stop words
				if word not in self.stop_words:
					if word in self.bookshelf.keys():
						self.bookshelf[word] += 1
					else:
						self.bookshelf[word] = 1
			'''

			self.count += 1

			# How often to update? Framerate will depend on the number of relevant 
			# tweets, so one size does not necessarily fit all			
			it = 5
			
			# Move forward
			if self.count % it == 0:
				sorted_words = sorted(self.bookshelf.items(), key=operator.itemgetter(1), reverse=True)
				
				clear()
				print('=== Update ==='.format(self.count))
				
				for i in range(0,20):
					print('{}): {} [{}]'.format(str(i+1),sorted_words[i][0],sorted_words[i][1]))


	def on_error(self, status_code, data):
		print(status_code)
		self.disconnect()


'''
The problem of lemmatization is often attacked algorithmically.

I personally think this is a mistake in syntatic processing (not
natural language processing). There aren't that many words, and
there aren't really that many plurals, posessions, intransitives, etc.

In such a limited space, I think we can hold this in memory. 

Consider common failures of the Porter Stemmer or the 
Lancaster Stemmer:

have -> hav
decide -> decid
police -> pol

Why not just enumerate the relationships as opposed to trying
to devine the stem? 

A huge thank you to Yasumasa Someya. In 1998, he made a great
map that is thorough and is just what is needed:

have <- has,having,had,'d,'ve,d,ve
decide <- decides,deciding,decided
police <- polices,policing,policed

1998 may seem some time ago now but thankfully, the delta-t on the English 
language is small.

The file e_lemma.txt courtesy of:
	http://lexically.net/downloads/BNC_wordlists/e_lemma.txt
'''


class YasumasaStemmer():
	'''
	Keep in mind how fickle this can be:
	When covering the 2016 election, sander -> sanders. . .
	'''
	def __init__(self):
		self.stems = {}
		with open('e_lemma.txt','r') as stems:
			for line in stems:
				line = line.replace('\n','')
				parsed = line.split(' -> ')
				alts = parsed[1].split(',')
				for a in alts:
					self.stems[a] = parsed[0]


def main(argv):
        print(argv[0:])
        stream = MyStreamer(credentials.key,credentials.secret,credentials.authkey,credentials.authsecret)
        stream.staging()

        keyword = argv[0:]
        stream.stop_words.append(keyword)
        stream.statuses.filter(track=keyword)

if __name__ == '__main__':
        main(sys.argv[1:])
