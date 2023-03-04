import uuid
from htrc.torchlite.ef.workset import WorkSet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords


def compose_n(*functions):
    def compose2(f, g):
        return lambda x: f(g(x))

    return functools.reduce(compose2, functions, lambda x: x)


def compose_1(f, g):
    return lambda x: f(g(x))


lem = WordNetLemmatizer()
stem = PorterStemmer()


class Filter(object):
    '''The base torchlite filter class'''

    def __init__(self, workset):
        self.id = uuid.uuid1()
        self.filters = None
        self._tokens = None
        self._data = None
        self.workset = workset
        self.type = "Generic"

    @property
    def tokens(self):
        if not self._tokens:
            self._tokens = self.workset.tokens.keys()
        return self._tokens

    @property
    def data(self):
        if self._data is None:
            self.refresh()
        return self._data

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id})"

    def add_filter(self, fn):
        if self.filters is None:
            self.filters = fn
        else:
            self.filters = compose(fn, self.filters)
        self.reset()

    def reset(self):
        self._data = None

    def refresh(self):
        self.reset()
        self.apply_filters()

    def apply_filters(self):
        if self._data is None:
            if self.filters is None:
                self._data = self.tokens
            else:
                self._data = self.filters(self.tokens)

    def stem_fn(self):
        def fn(toks):
            stemmer = PorterStemmer()
            return [stemmer.stem(tok) for tok in toks]

        return fn

    def lem_fn(self):
        def fn(toks):
            lem = WordNetLemmatizer()
            return [lem.lemmatize(tok) for tok in toks]

        return fn

    def stopword_fn(self):
        def fn(toks):
            return [tok for tok in toks if tok not in stopwords.words('english')]

        return fn


f = Filter(WorkSet('63f7ae452500006404fc54c7'))
