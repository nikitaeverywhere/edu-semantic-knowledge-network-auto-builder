from .Rule import Rule
from .utils import pick_groups


noun = Rule(['NN', 'NNS', 'NNP', 'NNPS'])
compound_noun = Rule()
compound_noun.extend([
	(noun, 'POS', compound_noun),  # princess's cat
	(noun, compound_noun),         # mister cat
	noun                           # cat
])
verb = Rule(['VB', 'VBZ', 'VBD', 'VBG', 'VBN', 'VBP'])
determiner = Rule(['DT', 'WDT', 'PDT'])
adverb = Rule([
	(determiner, 'RBS'),  # the biggest
	'RB',                 # occasionally, professionally
	'RBR'                 # bigger
])
adjective = Rule([
	(determiner, 'JJS'),  # the beautifulest
	'JJ',                 # beautiful
	'JJR'                 # beautifuler
])
list_of_adjectives = Rule()
list_of_adjectives.extend([
	(adjective, ',', list_of_adjectives),  # small, funny kid
	(adjective, list_of_adjectives),       # funny fast little
	adjective                              # fast
])
noun_with_adjectives = Rule([
	(list_of_adjectives, compound_noun),    # beautiful small garden
	compound_noun                           # good morning
])
concept = Rule([
	(adverb, adjective, noun),                    # even greater record
	(determiner, noun_with_adjectives),           # a car, a very nice car
	noun_with_adjectives                          # morning, good morning
])
baseFunctor = Rule([
	(verb, verb, 'PRP$'),  # is using our
	(verb, verb, 'IN'),    # shows in
	(verb, verb),          # is using
	(verb, 'PRP$'),        # use their
	(verb, 'IN'),          # shows in
	verb                   # using
])
functor = Rule([
	('MD', baseFunctor),
	baseFunctor
])

# Language rule set

english = Rule([
	(concept, functor, concept),             # a big man | likes | big girls
	(concept, 'IN', concept),                # a car in the truck
	(concept, functor, adverb, concept),     # cat | is | the cutest, professionally trained | pet
	(concept, functor, adverb, adjective),   # car | is | very | effective
	(concept, functor, adjective)            # drugs are harmful
], [
	pick_groups(1, 1, 1, 3),
	pick_groups(1, 1, 1, 3),
	pick_groups(1, 1, 2, 3),
	pick_groups(1, 1, 2, 3)
])
