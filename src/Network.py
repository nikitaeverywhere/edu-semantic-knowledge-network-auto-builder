from .utils import write_xlsx_file


class Network:

	def __init__(self, rule_set):
		"""
		:param rule_set: Rule
		"""
		self.edges = {}
		self.nodes = {}
		self.rule_set = rule_set
		pass

	def add_node(self, node_id, name, weight=1):
		if node_id not in self.nodes:
			self.nodes[node_id] = {
				'id': node_id,
				'names': {name},
				'weight': weight
			}
		else:
			self.nodes[node_id]['names'].add(name)
			self.nodes[node_id]['weight'] += weight

	def add_edge(self, from_id, to_id, name):
		if from_id not in self.nodes or to_id not in self.nodes:
			return
		edge_id = from_id + '|' + to_id
		if edge_id not in self.edges:
			self.edges[edge_id] = {
				'from': from_id,
				'to': to_id,
				'names': {name},
				'weight': (self.nodes[from_id]['weight'] + self.nodes[to_id]['weight']) / 2
			}
		else:
			self.edges[edge_id]['names'].add(name)
			self.edges[edge_id]['weight'] += \
				(self.nodes[from_id]['weight'] + self.nodes[to_id]['weight']) / 2

	def merge(self, text):
		""" Merge a new text to the network.
		:param text: Text instance with loaded text
		:return: Boolean
		"""
		index = 0
		while index < len(text.terms):
			words, context = self.rule_set.apply(text.terms, index)
			if len(words) == 0:
				index += 1
				continue
			if 'from' in context and 'to' in context and 'link' in context:
				from_base = context['from-base'] if 'from-base' in context else context['from']
				to_base = context['to-base'] if 'to-base' in context else context['to']
				self.add_node(from_base, context['from'])
				self.add_node(to_base, context['to'])
				self.add_edge(from_base, to_base, context['link'] if 'link' in context else '?')
			if 'index' in context:
				index = context['index']
			else:
				index += 1

	def save_graph(self, filename):
		""" Save network to a XLS file as a graph, consisting of nodes and edges.
		:param filename: string, filename without extension
		"""
		node_data = [["Id", "Label"]]
		edge_data = [["Source", "Target", "Id", "Label", "Weight"]]
		for node in self.nodes.values():
			node_data.append([node["id"], '\n'.join(list(node["names"]))])
		for edge in self.edges.values():
			edge_data.append([
				edge["from"],
				edge["to"],
				edge["from"] + '|' + edge["to"],
				'\n'.join(list(edge["names"])),
				edge["weight"]
			])
		write_xlsx_file(filename + "-nodes.xlsx", node_data)
		write_xlsx_file(filename + "-edges.xlsx", edge_data)
