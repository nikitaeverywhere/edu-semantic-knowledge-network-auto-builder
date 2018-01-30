from src.TextCorpus import TextCorpus
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
corpus = TextCorpus()

corpus.load_from_path(os.path.join(current_dir, 'datasets/bbc-news/news'))
corpus.serialize(os.path.join(current_dir, 'test.json'))
