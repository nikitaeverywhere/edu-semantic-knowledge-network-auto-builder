from copy import deepcopy


class Rule:

	def __init__(self, cases=None, mutations=None):
		self.cases = cases if cases is not None else []
		self.mutations = mutations if mutations is not None else []
		pass

	def extend(self, cases=None, mutations=None):
		if cases is not None:
			self.cases.extend(cases)
		if mutations is not None:
			self.mutations.extend(mutations)

	def case(self, n):
		return self.cases[n]

	def mutate(self, context, n, term_groups):
		# [['very', 'beautiful', 'flower'], ['shocks'], ['me']]
		if n >= len(self.mutations):
			return context
		mutation = self.mutations[n]
		for prop, fun in mutation.items():
			context[prop] = fun(groups=term_groups)
		return context

	def apply(self, text, index, context=None):
		"""
		Try to apply rules at the text at particular position pos.
		:param text:
		:param index: index to search from
		:param context: optional context
		:return: (['matched', 'terms', 'if', 'any'], { 'context': 'dict' })
		"""
		if context is None:
			context = {}

		for n, seq in enumerate(self.cases):  # [..., ..., ...]
			if not isinstance(seq, tuple):
				seq = tuple([seq])
			term_groups = []
			ctx = deepcopy(context)
			pos = index
			for case in seq:  # (..., ..., ...)
				if pos >= len(text):
					break
				if isinstance(case, str):
					if text[pos][1] == case:
						term_groups.append([text[pos]])
						pos += 1
						# return [text[pos][0]], self.mutate(context, n, [[text[pos][0]]])
					else:
						break
				if isinstance(case, Rule):
					rule_terms, ctx = case.apply(text, pos, ctx)
					if len(rule_terms) > 0:
						term_groups.append(rule_terms)
						pos += len(rule_terms)
						# return [res[0]], self.mutate(res[1], n, [res[0]])
					else:
						break
			else:  # executed if for (..., ..., ...) loop exits normally
				ctx = self.mutate(ctx, n, term_groups)
				terms = []
				for group in term_groups:
					for term in group:
						terms.append(term)
				return terms, ctx

		return [], {}

