#!/usr/bin/env python3

from src.TextCorpus import TextCorpus
from src.Text import Text
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
text_filename = os.path.join(
	current_dir, 'datasets/bbc-news/news/tech/ink-helps-drive-democracy-in-asia.txt'
)

corpus = TextCorpus(os.path.join(current_dir, 'datasets/bbc-news.json'))
text = Text(corpus, open(text_filename, mode='r', encoding='utf-8').read())

print(text.terms)
print(text.avg_score)
