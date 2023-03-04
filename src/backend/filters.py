import uuid
import nltk
from htrc.torchlite.ef.workset import WorkSet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from functools import reduce


def torchlite_stemmer(token_list):
    stemmer = PorterStemmer()
    return [stemmer.stem(tok) for tok in token_list]


def torchlite_lemmatizer(token_list):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(tok) for tok in token_list]


def torchlite_stopword_filter(token_list):
    return [tok for tok in token_list if tok not in stopwords.words('english')]


class Filter(object):
    def __init__(self, *fns):
        self.id = uuid.uuid1()
        self.type = "Generic"

        self.filters = reduce(lambda f, g: lambda x: g(f(x)), fns, lambda x: x)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id})"

    def add_filter(self, fn):
        if self.filters is None:
            self.filters = fn
        else:
            self.filters = compose(fn, self.filters)

    def apply(self, token_list):
        return self.filters(token_list)


ws = WorkSet('63f7ae452500006404fc54c7')
f = Filter()
