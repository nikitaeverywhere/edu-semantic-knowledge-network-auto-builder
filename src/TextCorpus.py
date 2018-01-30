import glob
import os
import json
from nltk import word_tokenize, pos_tag
from utils import get_word_normal_form, is_word


class TextCorpus:

	def __init__(self):
		self.words = {}
		pass

	def load_from_path(self, path, max_files=9223372036854775807):
		self.words = {}
		n = 0
		path = os.path.normpath(path)
		pattern = os.path.normpath(os.path.join(path, '**/*.*'))
		print('Loading files in ' + pattern)
		files = 0
		total_files = sum([len(files) for r, d, files in os.walk(path)])
		for filename in glob.iglob(
			os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.normpath(pattern)),
			recursive=True
		):
			files += 1
			print('Files: ' + str(files) + '/' + str(total_files) + ', terms: ' + str(n), end='\r')
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
				if normalized_word in self.words:
					self.words[normalized_word] += 1
				else:
					self.words[normalized_word] = 1
					n += 1
		print(
			'Files: ' + str(files) + '/' + str(total_files) + ', terms: ' + str(n)
			+ '; Load complete!'
		)

	def serialize(self, filename):
		open(filename, 'w', encoding='utf8').write(json.dumps(self.words, ensure_ascii=False))
