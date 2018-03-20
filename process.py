#!/usr/bin/env python3

from src.TextCorpus import TextCorpus
from src.Text import Text
from src.Network import Network
from src.rule_set import english
import os
import glob

current_dir = os.path.dirname(os.path.abspath(__file__))
df_filename = os.path.normpath(os.path.join(current_dir, 'datasets/bbc-news.json'))
texts_path = os.path.normpath(os.path.join(current_dir, 'input'))

print('Loading DF metrics from ')
corpus = TextCorpus(df_filename)

print('Creating English semantic network...')
net = Network(english)
print('Reading texts from ' + texts_path)
for filename in glob.iglob(os.path.join(texts_path, '**/*.*'), recursive=True):
	text = Text(corpus, open(filename, mode='r', encoding='utf-8').read())
	print('Text of ' + str(len(text.terms)) + ' terms with average score of ' + str(text.avg_score))
	net.merge(text)

net.save_graph('output/output')
net.log_to_html()
print('Graph saved to ' + current_dir + '/output/output-edges.xlsx (output-nodes.xlsx)!')
