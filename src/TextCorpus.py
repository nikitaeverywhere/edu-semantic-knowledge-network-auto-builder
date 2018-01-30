import glob
import os
import json
from nltk import word_tokenize, pos_tag
from .utils import get_word_normal_form, is_word
from collections import OrderedDict
from operator import itemgetter
import math


class TextCorpus:

	def __init__(self, json_file=''):
		self.data = self.get_initial_data() if json_file == '' else self.deserialize(json_file)
		pass

	@staticmethod
	def get_initial_data():
		return {
			'documents': 0,
			'termFrequencies': {}
		}

	def get_idf(self, term):
		return math.log(
			self.data['documents'] / max(1, min(1 + (
				self.data['termFrequencies'][term] if term in self.data['termFrequencies'] else 0
			), self.data['documents']))
		)

	def load_from_path(self, path, max_files=9223372036854775807):
		data = self.get_initial_data()
		n = 0
		path = os.path.normpath(path)
		pattern = os.path.normpath(os.path.join(path, '**/*.*'))
		print('Loading files in ' + pattern)
		files = 0
		data['documents'] = sum([len(files) for r, d, files in os.walk(path)])
		for filename in glob.iglob(
			os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.normpath(pattern)),
			recursive=True
		):
			files += 1
			print(
				'Files: ' + str(files) + '/' + str(data['documents']) + ', terms: ' + str(n),
				end='\r'
			)
			words_in_this_file = set()
			if files > max_files:
				break
			try:
				all_text = open(filename, mode='r', encoding='utf-8').read()
			except UnicodeDecodeError:
				print('\r\nUnable to decode file ' + filename + ' as UTF-8, skipping...')
				continue
			tagged = pos_tag(word_tokenize(all_text))  # See nltk.help.upenn_tagset() for tags info
			for (word, tag) in tagged:
				if not is_word(word, tag):
					continue
				normalized_word = get_word_normal_form(word, tag)
				if normalized_word in words_in_this_file:
					continue
				words_in_this_file.add(normalized_word)
				if normalized_word in data['termFrequencies']:
					data['termFrequencies'][normalized_word] += 1
				else:
					data['termFrequencies'][normalized_word] = 1
					n += 1
		print(
			'Files: ' + str(files) + '/' + str(data['documents']) + ', terms: ' + str(n)
			+ '; Load complete!'
		)
		self.data = data

	def serialize(self, filename):
		data = self.data.copy()
		data['termFrequencies'] = OrderedDict(
			sorted(data['termFrequencies'].items(), key=itemgetter(1), reverse=True)
		)
		open(filename, 'w', encoding='utf8').write(
			json.dumps(data, ensure_ascii=False, separators=(',', ':'))
		)

	def deserialize(self, filename):
		if not os.path.isfile(filename):
			return self.data
		try:
			self.data = json.loads(open(filename, 'r', encoding='utf8').read(), encoding='utf8')
		except json.decoder.JSONDecodeError:
			return self.data
		return self.data
