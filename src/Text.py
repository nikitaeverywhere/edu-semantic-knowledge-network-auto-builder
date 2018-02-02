from nltk import word_tokenize, pos_tag
from .utils import get_word_normal_form, is_word
from collections import Counter


class Text:

	def __init__(self, corpus, text='no text'):
		self.avg_score = 0
		self.max_score = 0
		self.terms = []
		self.used_terms = set()  # positions of used terms
		self.considered_terms = set()
		self.load_text(text, corpus)
		pass

	def mark_terms_as_used(self, index, length=1):
		i = 0
		while i < length:
			self.used_terms.add(i + index)
			i += 1

	def mark_terms_as_considered(self, index, length=1):
		i = 0
		while i < length:
			self.considered_terms.add(i + index)
			i += 1

	def load_text(self, text, corpus):

		words = []
		terms = []
		tokenized = pos_tag(word_tokenize(text))

		# first pass: pick term frequencies
		for pair in tokenized:
			if is_word(pair[0], pair[1]):
				words.append(get_word_normal_form(pair[0], pair[1]))
		term_freq = Counter(words)

		# second pass: form output array and find average score
		n = 0
		total_score = 0
		for pair in tokenized:
			if not is_word(pair[0], pair[1]):
				terms.append((pair[0], pair[1], 0, pair[0]))
				continue
			word_normalized = get_word_normal_form(pair[0], pair[1])
			score = term_freq[word_normalized] * corpus.get_idf(word_normalized)
			n += 1
			total_score += score
			if score > self.max_score:
				self.max_score = score
			terms.append((
				word_normalized,  # normalized word
				pair[1],          # tag
				score,            # raw tf-idf value
				pair[0]           # original word
			))
		self.avg_score = total_score / n

		self.terms = terms
		return terms
