from .utils import write_xlsx_file
from os import path
import json


def list_append(lst, item):
	lst.append(item)
	return lst


current_dir = path.dirname(path.abspath(__file__))
in_html_file = path.normpath(path.join(current_dir, 'usage.html'))
out_html_file = path.normpath(path.join(current_dir, '../output/usage.html'))


class Network:

	def __init__(self, rule_set):
		"""
		:param rule_set: Rule
		"""
		self.edges = {}
		self.nodes = {}
		self.rule_set = rule_set
		self.texts = []
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

		self.texts.append(text)
		index = 0
		threshold = text.avg_score

		while index < len(text.terms):

			terms, context = self.rule_set.apply(text.terms, index)
			if len(terms) == 0:
				index += 1
				continue
			text.mark_terms_as_considered(index, len(terms))

			max_score_in_group = 0
			for term in terms:
				if term[2] > max_score_in_group:
					max_score_in_group = term[2]
			if max_score_in_group < threshold:
				index += 1
				continue

			text.mark_terms_as_used(index, len(terms))
			if 'from' in context and 'to' in context and 'link' in context:
				from_base = context['from-base'] if 'from-base' in context else context['from']
				to_base = context['to-base'] if 'to-base' in context else context['to']
				self.add_node(from_base, context['from'])
				self.add_node(to_base, context['to'])
				self.add_edge(from_base, to_base, context['link'] if 'link' in context else '?')
			if 'index' in context:
				index += context['index']
			else:
				index += 1

	def save_graph(self, filename):
		""" Save network to a XLS file as a graph, consisting of nodes and edges.
		:param filename: string, filename without extension
		"""
		node_data = [["Id", "Label"]]
		edge_data = [["Source", "Target", "Id", "Label", "Weight"]]
		for node in self.nodes.values():
			node_data.append([node["id"], ', '.join(list(node["names"]))])
		for edge in self.edges.values():
			edge_data.append([
				edge["from"],
				edge["to"],
				edge["from"] + '->' + edge["to"],
				', '.join(list(edge["names"])),
				1
			])
		write_xlsx_file(filename + "-nodes.xlsx", node_data)
		write_xlsx_file(filename + "-edges.xlsx", edge_data)

	def log_to_html(self):
		print('Logging results to ' + out_html_file + '...', end='')
		data = {
			'texts': []
		}
		for text in self.texts:
			data['texts'].append({
				'entities': [
					{
						'id': x[0],
						'tag': x[1],
						'score': x[2],
						'text': x[3],
						'used': i in text.used_terms,
						'considered': i in text.considered_terms
					} for i, x in enumerate(text.terms)
				],
				'maxScore': text.max_score,
				'avgScore': text.avg_score
			})

		content = open(in_html_file, 'r', encoding='utf8').read() \
			.replace('/*replace:data*/', json.dumps(data, ensure_ascii=False))
		open(out_html_file, 'w', encoding='utf8').write(content)
		print(' Done.')
