class Rule:

	def __init__(self, desc=list()):
		self.desc = desc
		pass

	def extend(self, rule_set=list()):
		for rule in rule_set:
			self.desc.append(rule)
