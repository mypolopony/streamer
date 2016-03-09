import os
import operator
from twython import TwythonStreamer
from nltk.stem.lancaster import LancasterStemmer # I really don't like this stemmer but it's standard

## As always, wayward home for lost but global variables (and functions!)
clear = lambda: os.system('cls')
st = LancasterStemmer()

class MyStreamer(TwythonStreamer):
	def staging(self):
		self.bookshelf = dict()
		self.count = 0

		with open('stop_words.txt','r') as sw:
			self.stop_words = sw.read().splitlines()

	
	def on_success(self, data):
		# Digest
		if 'text' in data:
			line = data['text']
			for word in line.split(' '):
				word = word.lower()
				if word not in self.stop_words:
					if word in self.bookshelf.keys():
						self.bookshelf[word] += 1
					else:
						self.bookshelf[word] = 1
			self.count += 1
			
			it = 5
			
			# Move forward
			if self.count % it == 0:
				sorted_words = sorted(self.bookshelf.items(), key=operator.itemgetter(1), reverse=True)
				
				print('=== Update ==='.format(self.count))
				
				for i in range(0,20):
					print('{}): {} [{}]'.format(str(i+1),sorted_words[i][0],sorted_words[i][1]))

				

	def on_error(self, status_code, data):
		print(status_code)
		self.disconnect()



key = 'cok4sOTC7tX3J5ughI3rFpbSx'
secret = 'QSia5RKFdloXDi6DUq2MwnpGP49eSTCtySvljIJqYh4fLS0vmj'

authkey = '1217553746-TuFJgNC79p2uoAPlstnqkM9HoTOb7NsEkVmIGYx'
authsecret = 'X7jB10iBsgQrnTN9O1T8k7R7Ii8ZdNGAnMRAil3XU8CUS'

'''
The problem of lemmatization is often attacked algorithically.

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

#with open('e_lemma.txt','r'):

stream = MyStreamer(key,secret,authkey,authsecret)
stream.staging()
keyword = 'trump'
stream.stop_words.append(keyword)
stream.statuses.filter(track=keyword)

