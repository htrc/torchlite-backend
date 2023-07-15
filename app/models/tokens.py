import re
from pydantic import BaseModel
from typing import Optional, TypedDict
from collections import Counter, namedtuple


class PoSCnt(TypedDict):
    pos: str
    tally: int


class TokenPosCount(BaseModel):
    token: str
    poscounts: dict


class Token:
    def __init__(self, string: str, pos: Optional[str] = None) -> None:
        self.id: int
        self._raw: str = string
        self._text: str = self.normalize(self._raw)
        self._pos = pos
        if self._pos:
            self.id = hash(self._text + self._pos)
        else:
            self.id = hash(self._text)

    def normalize(self, input: str) -> str:
        new = input.strip()
        new = new.casefold()
        new = re.sub(r"\W+", "", new)
        return new

    def __repr__(self) -> str:
        return f"Token({self._text}, {self._pos})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return NotImplemented
        return self.id == other.id


TokenCount = namedtuple("TokenCount", "token counter")


class TokenCounter:
    def __init__(self) -> None:
        self.index: dict = {}
        self.counter: Counter = Counter()

    def add(self, tcnt: TokenCount) -> None:
        self.index[tcnt.token._text] = tcnt.token.id
        self.counter.update(tcnt.counter)

    def count_of(self, key: str) -> int | None:
        try:
            tokid = self.index[key]
            return self.counter.get(tokid)
        except KeyError:
            print(f"{key} not in the counter")
            return None


def parse_ef_token(tok: str, pos_dict: dict) -> list[Token]:
    result: list = []
    for pos, cnt in pos_dict.items():
        token: Token = Token(tok, pos)
        cntr: Counter = Counter()
        cntr[token.id] = cnt
        result.append(TokenCount(token=token, counter=cntr))
    return result


def tokensCount(token_counts: dict) -> list:
    result: list = []
    for tok, cnt in token_counts.items():
        token = Token(tok)
        cntr = Counter({token.id: cnt})
        result.append(TokenCount(token=token, counter=cntr))
    return result


def tokenPosCount(tok_pos_count: dict) -> list:
    result: list = []
    for tok, pos_dict in tok_pos_count.items():
        for pos, cnt in pos_dict.items():
            token = Token(tok, pos)
            cntr = Counter({token.id: cnt})
            result.append(TokenCount(token=token, counter=cntr))
    return result
