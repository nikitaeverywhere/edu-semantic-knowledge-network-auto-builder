import glob
import re
import os
import json

current_dir = os.path.dirname(__file__)
regex = re.compile('[^.,;():?!"\'\s]+(?:\'[sd])?')


def normalize_words(words):
	normalized = []
	for word in words:
		lower = word.lower()
		if lower == 'it\'s':
			normalized.append('it')
			normalized.append('is')
			continue
		if len(lower) > 2 and lower[-2] == '\'':
			if lower[-1] == 'd':
				normalized.append(lower[:-2])
				normalized.append('would')
				continue
			if lower[-1] == 's':
				lower = lower[:-2]
				if len(lower) == 0:
					continue
		normalized.append(lower)
	return normalized


class TextCorpus:

	def __init__(self):
		self.words = {}
		pass

	def load_from_path(self, path, max_files=9223372036854775807):
		self.words = {}
		pattern = os.path.join(path, '**/*.*')
		files = 0
		for filename in glob.iglob(
			os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.normpath(pattern)),
			recursive=True
		):
			files += 1
			words_in_this_file = set()
			if files > max_files:
				break
			all_text = open(filename, 'r').read()
			words = regex.findall(all_text)
			for word in normalize_words(words):
				if word in words_in_this_file:
					continue
				words_in_this_file.add(word)
				if word in self.words:
					self.words[word] += 1
				else:
					self.words[word] = 1

	def serialize(self, filename):
		open(filename, 'w').write(json.dumps(self.words))
