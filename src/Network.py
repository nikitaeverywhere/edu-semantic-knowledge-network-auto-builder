from .utils import is_word, write_xlsx_file


class Network:

	def __init__(self, rule_set):
		self.edges = {}
		self.nodes = {}
		self.rule_set = rule_set
		pass

	def merge(self, text):
		""" Merge a new text to the network.
		:param text: Text instance with loaded text
		:return: Boolean
		"""
		threshold = text.avg_score
		# todo

	def save_graph(self, filename):
		""" Save network to a XLS file as a graph, consisting of nodes and edges.
		:param filename: string, filename without extension
		"""
		node_data = [["Id", "Label"]]
		edge_data = [["Source", "Target", "Id", "Label", "Weight"]]
		edge_id = 0
		for node in self.nodes.values():
			node_data.append([node["id"], node["label"]])
		for edge in self.edges.values():
			for label in edge["labels"]:
				edge_data.append([edge["source"], edge["target"], edge_id, label, edge["weight"]])
				edge_id += 1
		write_xlsx_file(filename + "-nodes.xlsx", node_data)
		write_xlsx_file(filename + "-edges.xlsx", edge_data)
