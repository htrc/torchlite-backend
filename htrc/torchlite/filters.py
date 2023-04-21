import uuid
from collections import Counter
from functools import reduce

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer


def torchlite_stemmer(token_list: Counter):
    stemmer = PorterStemmer()
    new_list = Counter()
    for token, token_count in token_list.items():
        new_list[stemmer.stem(token)] += token_count
    return new_list


def torchlite_lemmatizer(token_list: Counter):
    lemmatizer = WordNetLemmatizer()
    new_list = Counter()
    for token, token_count in token_list.items():
        new_list[lemmatizer.lemmatize(token)] += token_count
    return new_list


def torchlite_stopword_filter(token_list: Counter):
    """Token_list is a Counter"""
    new_list = Counter()
    stoplist = stopwords.words("english")
    for token, token_count in token_list.items():
        if token not in stoplist:
            new_list[token] += token_count
    return new_list


class Filter(object):
    def __init__(self, *fns):
        self.id = uuid.uuid1()
        self.type = "Generic"
        self.filter_fns = fns

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id})"

    def compose(self, f, g):
        return lambda x: g(f(x))

    def apply(self, token_list):
        fn = reduce(self.compose, self.filter_fns, lambda x: x)
        return fn(token_list)


class FilterFactory(object):
    def __init__(self):
        self.registry = {}

    def register(self, key, fn):
        self.registry[key] = fn

    def make_filter(self, fnames):
        filter_fns = [self.registry[fname] for fname in fnames]
        return Filter(*filter_fns)
