import os
import operator
from twython import TwythonStreamer

## As always, wayward home for lost but global variables (and functions!)
clear = lambda: os.system('cls')

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
			
			it = 100
			
			# Move forward
			if self.count % it == 0:
				sorted_words = sorted(self.bookshelf.items(), key=operator.itemgetter(1), reverse=True)
				
				print('=== Update ==='.format(self.count))
				
				for i in range(0,10):
					print('{}): {} [{}]'.format(str(i+1),sorted_words[i][0],sorted_words[i][1]))

				

	def on_error(self, status_code, data):
		print(status_code)
		self.disconnect()



key = 'cok4sOTC7tX3J5ughI3rFpbSx'
secret = 'QSia5RKFdloXDi6DUq2MwnpGP49eSTCtySvljIJqYh4fLS0vmj'

authkey = '1217553746-TuFJgNC79p2uoAPlstnqkM9HoTOb7NsEkVmIGYx'
authsecret = 'X7jB10iBsgQrnTN9O1T8k7R7Ii8ZdNGAnMRAil3XU8CUS'

stream = MyStreamer(key,secret,authkey,authsecret)
stream.staging()
stream.statuses.filter(track='love')

