import functools
import regex as re

from re import Pattern
from collections import Counter
from typing import Literal, Set

from .base import WidgetBase, WidgetDataTypes
from ..ef import models as ef_models
from ..ef.models import VolumeAggFeaturesNoPos

class SimpleTagCloudWidget(WidgetBase):
    type: Literal['SimpleTagCloud'] = 'SimpleTagCloud'
    data_type: WidgetDataTypes = WidgetDataTypes.agg_vols_no_pos

    
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
            "same,so,than,too,very,say,says,said,shall,the,`,``,|".split(","))
    )
    
    punctuation_and_numbers_regex: str = r'[\p{P}\d]'
    _regex: Pattern = re.compile(punctuation_and_numbers_regex)

    @staticmethod
    def aggregate_counts(p1: dict, p2: dict) -> dict:
        p1_counter = Counter(p1)
        p2_counter = Counter(p2)

        return p1_counter + p2_counter

    @staticmethod
    def aggregate_word_counts(word_counts: dict) -> dict:
        aggregated_counts = {}

        if word_counts:
            for word, count in word_counts.items():
                lower_word = word.lower()

                if lower_word in aggregated_counts:
                    aggregated_counts[lower_word] += count
                else:
                    aggregated_counts[lower_word] = count

        return aggregated_counts

    async def get_data(self, volumes: list[ef_models.Volume[VolumeAggFeaturesNoPos]]) -> dict:
        print("get_data simple_tag_cloud A")
        vol_token_counts = [
            self.aggregate_word_counts(volume.features.body)
            for volume in volumes
        ]
        print("get_data simple_tag_cloud B")
        token_counts = functools.reduce(self.aggregate_counts, vol_token_counts)
        token_counts = [
            (k, v) for k, v in token_counts.items()
            if len(k) > 2 and k not in self.stopwords and not re.search(self._regex, k)
        ]
        # FIXME: all these conditions should probably be input parameters to the widget that can be controlled from
        #        the frontend rather than hardcoded here
        print("get_data simple_tag_cloud C")
        token_counts = sorted(token_counts, key=lambda x: x[1], reverse=True)[:100]
        print("get_data simple_tag_cloud D")
        return dict(token_counts)
