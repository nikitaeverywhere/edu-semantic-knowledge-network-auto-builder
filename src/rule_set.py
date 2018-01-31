from .Rule import Rule

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
	'RB',                # occasionally, professionally
	'RBR',               # bigger
	(determiner, 'RBS')  # the biggest
])
adjective = Rule([
	'JJ',                # beautiful
	'JJR',               # beautifuler
	(determiner, 'JJS')  # the beautifulest
])
list_of_adjectives = Rule()
list_of_adjectives.extend([
	(adjective, list_of_adjectives),   # funny fast little
	adjective                          # fast
])
noun_with_adjectives = Rule([
	compound_noun,                          # good morning
	(list_of_adjectives, compound_noun)     # beautiful small garden
])
concept = Rule([
	noun_with_adjectives,                         # morning, good morning
	(determiner, noun_with_adjectives),           # a car, a very nice car
])
functor = Rule([
	verb,                 # using
	(verb, verb),         # is using
	(verb, 'PRP$'),       # using their
	(verb, verb, 'PRP$')  # is using our
])

# Language rule set

english = Rule([
	(concept, functor, concept),             # a big man | likes | big girls
	(concept, functor, adverb, concept),     # cat | is | the cutest, professionally trained | pet
	(concept, functor, adverb, adjective)    # car | is | very | effective
], [
	{
		'from-base': lambda term_groups: term_groups[0][-1],
		'from': lambda term_groups: ' '.join(term_groups[0]),
		'link': lambda term_groups: ' '.join(term_groups[1]),
		'to-base': lambda term_groups: term_groups[2][-1],
		'to': lambda term_groups: ' '.join(term_groups[2])
	}
])
