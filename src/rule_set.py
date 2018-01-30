from .Rule import Rule

noun = Rule(['NN', 'NNS', 'NNP', 'NNPS'])
compound_noun = Rule()
compound_noun.extend(tuple([noun, compound_noun]))
verb = Rule(['VB', 'VBZ', 'VBD', 'VBG', 'VBN'])
adverb = Rule(['RB', 'RBR', 'RBS'])
adjective = Rule(['JJ', 'JJR', 'JJS'])
list_of_adjectives = Rule()
list_of_adjectives.extend(tuple([adjective, list_of_adjectives]))
concept = Rule([
	compound_noun,
	('DT', compound_noun),
	(list_of_adjectives, compound_noun),
])
functor = Rule([
	verb
])

# Language rule set

english = Rule([
	(concept, verb, concept),
	(concept, verb, 'RP', concept),
	(concept, verb, adverb, adjective)
])
