from .Rule import Rule
from functools import reduce
from .utils import clean_the


noun = Rule(['NN', 'NNS', 'NNP', 'NNPS', 'PRP'])
compound_noun = Rule()
compound_noun.extend([
	(noun, 'POS', compound_noun),  # princess's cat
	(noun, compound_noun),         # mister cat
	noun                           # cat
])
verb = Rule(['VB', 'VBZ', 'VBD', 'VBG', 'VBN'])
determiner = Rule(['DT', 'WDT', 'PDT'])
adverb = Rule([
	(determiner, 'RBS'),  # the biggest
	'RB',                 # occasionally, professionally
	'RBR'                # bigger
])
adjective = Rule([
	(determiner, 'JJS'),  # the beautifulest
	'JJ',                 # beautiful
	'JJR'                 # beautifuler
])
list_of_adjectives = Rule()
list_of_adjectives.extend([
	(adjective, list_of_adjectives),   # funny fast little
	adjective                          # fast
])
noun_with_adjectives = Rule([
	(list_of_adjectives, compound_noun),    # beautiful small garden
	compound_noun                           # good morning
])
concept = Rule([
	(determiner, noun_with_adjectives),           # a car, a very nice car
	noun_with_adjectives                          # morning, good morning
])
functor = Rule([
	(verb, verb, 'PRP$'),  # is using our
	(verb, verb),          # is using
	(verb, 'PRP$'),        # using their
	verb                   # using
])


# Language rule set

english = Rule([
	(concept, functor, concept),             # a big man | likes | big girls
	(concept, functor, adverb, concept),     # cat | is | the cutest, professionally trained | pet
	(concept, functor, adverb, adjective)    # car | is | very | effective
], [
	{
		'from-base': lambda **a: a['groups'][0][-1],
		'from': lambda **a: ' '.join(clean_the(a['groups'][0])),
		'link': lambda **a: ' '.join(a['groups'][1]),
		'to-base': lambda **a: a['groups'][2][-1],
		'to': lambda **a: ' '.join(clean_the(a['groups'][2])),
		'index': lambda **a:
			a['index'] + reduce(lambda acc, terms: acc + len(terms), a['groups'][:-1], 0)
	},
	{
		'from-base': lambda **a: a['groups'][0][-1],
		'from': lambda **a: ' '.join(clean_the(a['groups'][0])),
		'link': lambda **a: ' '.join(a['groups'][1]),
		'to-base': lambda **a: a['groups'][3][-1],
		'to': lambda **a: ' '.join(clean_the(a['groups'][2])) + ' ' + ' '.join(clean_the(a['groups'][3])),
		'index': lambda **a:
			a['index'] + reduce(lambda acc, terms: acc + len(terms), a['groups'][:-1], 0)
	},
	{
		'from-base': lambda **a: a['groups'][0][-1],
		'from': lambda **a: ' '.join(clean_the(a['groups'][0])),
		'link': lambda **a: ' '.join(a['groups'][1]),
		'to-base': lambda **a: a['groups'][3][-1],
		'to': lambda **a: ' '.join(clean_the(a['groups'][2])) + ' ' + ' '.join(clean_the(a['groups'][3])),
		'index': lambda **a:
			a['index'] + reduce(lambda acc, terms: acc + len(terms), a['groups'][:-1], 0)
	}
])
