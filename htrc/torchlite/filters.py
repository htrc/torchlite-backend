from typing import Any, Callable, List, Optional, Sequence
import uuid
from collections import Counter
from functools import reduce

from nltk.corpus import stopwords #type: ignore
from nltk.stem import PorterStemmer, WordNetLemmatizer #type: ignore


def torchlite_stemmer(token_list: Counter) -> Counter:
    stemmer: PorterStemmer = PorterStemmer()
    new_list: Counter = Counter()
    for token, token_count in token_list.items():
        new_list[stemmer.stem(token)] += token_count
    return new_list


def torchlite_lemmatizer(token_list: Counter) -> Counter:
    lemmatizer: WordNetLemmatizer = WordNetLemmatizer()
    new_list: Counter = Counter()
    for token, token_count in token_list.items():
        new_list[lemmatizer.lemmatize(token)] += token_count
    return new_list


def torchlite_stopword_filter(token_list: Counter) -> Counter:
    """Token_list is a Counter"""
    new_list: Counter = Counter()
    stoplist: List = stopwords.words("english")
    for token, token_count in token_list.items():
        if token not in stoplist:
            new_list[token] += token_count
    return new_list


class Filter(object):
    def __init__(self, *fns: Optional[Callable]) -> None:
        self.id: uuid.UUID = uuid.uuid1()
        self.type: str = "Generic"
        self.filter_fns: Sequence = fns

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id})"

    def compose(self, f: Callable, g: Callable) -> Callable:
        return lambda x: g(f(x))

    def apply(self, token_list: Counter) -> Any:
        if self.filter_fns:
            filter_fn: Callable = reduce(self.compose, self.filter_fns, lambda x: x)
            return filter_fn(token_list)


class FilterFactory(object):
    def __init__(self) -> None:
        self.registry: dict[str, Callable] = {}

    def register(self, key: str, fn: Callable) -> None:
        self.registry[key] = fn

    def make_filter(self, fnames: List[str]) -> Filter:
        filter_fns: List[Callable] = [self.registry[fname] for fname in fnames]
        return Filter(*filter_fns)
