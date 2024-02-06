import functools
import regex as re

from re import Pattern
from collections import Counter
from typing import Literal, Set

from .base import WidgetBase, WidgetDataTypes
from ..ef import models as ef_models


class SimpleTagCloudWidget(WidgetBase):
    type: Literal['SimpleTagCloud'] = 'SimpleTagCloud'
    data_type: WidgetDataTypes = WidgetDataTypes.vols_no_pos

    stopwords: Set[str] = (
        set("i,me,my,myself,we,us,our,ours,ourselves,you,your,yours,yourself,yourselves,he,him,his,himself,"
            "she,her,hers,herself,it,its,itself,they,them,their,theirs,themselves,what,which,who,whom,whose,"
            "this,that,these,those,am,is,are,was,were,be,been,being,have,has,had,having,do,does,did,doing,will,"
            "would,should,can,could,ought,i'm,you're,he's,she's,it's,we're,they're,i've,you've,we've,they've,"
            "i'd,you'd,he'd,she'd,we'd,they'd,i'll,you'll,he'll,she'll,we'll,they'll,isn't,aren't,wasn't,"
            "weren't,hasn't,haven't,hadn't,doesn't,don't,didn't,won't,wouldn't,shan't,shouldn't,can't,cannot,"
            "couldn't,mustn't,let's,that's,who's,what's,here's,there's,when's,where's,why's,how's,a,an,the,and,"
            "but,if,or,because,as,until,while,of,at,by,for,with,about,against,between,into,through,during,"
            "before,after,above,below,to,from,up,upon,down,in,out,on,off,over,under,again,further,then,once,"
            "here,there,when,where,why,how,all,any,both,each,few,more,most,other,some,such,no,nor,not,only,own,"
            "same,so,than,too,very,say,says,said,shall,the".split(","))
    )

    punctuation_regex: str = r'\p{P}'

    _punct_regex: Pattern = re.compile(punctuation_regex)

    @staticmethod
    def aggregate_counts(p1: dict, p2: dict) -> dict:
        p1_counter = Counter(p1)
        p2_counter = Counter(p2)

        return p1_counter + p2_counter

    @staticmethod
    def lowercase(d: dict) -> dict:
        return {k.lower(): v for k, v in d.items()}

    async def get_data(self, volumes: list[ef_models.Volume]) -> dict:
        pages_with_tokens = [
            self.lowercase(page.body.tokens_count)
            for volume in volumes
            for page in volume.features.pages if page.body.tokens_count
        ]

        token_counts = functools.reduce(self.aggregate_counts, pages_with_tokens)
        return {
            k: v for k, v in token_counts.items()
            if k not in self.stopwords and (not self.punctuation_regex or not re.search(self._punct_regex, k))
        }
