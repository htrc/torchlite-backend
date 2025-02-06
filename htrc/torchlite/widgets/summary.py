from typing import Literal, TypeAlias

from .base import WidgetBase, WidgetDataTypes
from ..ef import models as ef_models
from ..ef.models import VolumeAggFeaturesNoPos


class SummaryWidget(WidgetBase):
    type: Literal['Summary'] = 'Summary'
    data_type: WidgetDataTypes = WidgetDataTypes.agg_vols_no_pos

    async def get_data(self, volumes: list[ef_models.Volume[VolumeAggFeaturesNoPos]]) -> dict:
        def update_dict(tokenDict: dict, resultsDict: dict) -> None:
            if tokenDict:
                for token, count in tokenDict.items():
                    lowercaseToken = token.lower()
                    resultsDict[lowercaseToken] = (resultsDict[lowercaseToken] if lowercaseToken in resultsDict else 0) + count

        def updatedset(token_dict: dict, unique_word_forms: dict, volumeid: str) -> None:
            if token_dict:
                for token, count in token_dict.items():
                    lowercaseToken = token.lower()
                    
                    if volumeid in unique_word_forms:
                        unique_word_forms[volumeid].add(lowercaseToken)
                    else:
                        #If the volume identifier doesn't exist, create a new set with the token
                        unique_word_forms[volumeid] = set([lowercaseToken])

        def calculate_readability(num_words: int) -> float:
            avg_words_per_sentence = 15  
            avg_syllables_per_word = 1.2  

            num_sentences = num_words / avg_words_per_sentence
            num_syllables = num_words * avg_syllables_per_word

            readability_score = 0.39 * (num_words / num_sentences) + 11.8 * (num_syllables / num_words) - 15.59
            return readability_score
        
        Extremes: TypeAlias = Literal['max','min']        
        def find_extreme_value(target: dict, extreme: Extremes) -> str:
            sortedDocuments = sorted(list(target.keys()), key=lambda a: target[a]['value'], reverse=(True if extreme == 'max' else False))
            limitedDocuments = sortedDocuments[:5]
            return ';  '.join([f"{target[doc]['title']} ({target[doc]['value']})" for doc in limitedDocuments])
        print("get_data summary A")
        total = 0
        totalunique = 0
        loacalPerVolDict = {}
        per_vol_set = {}
        #frequentWords = {}

        document_lengths = {}
        document_words = {}
        vocab_density = {}
        #readability_score = {}
        #read_score = 0

        for volume in volumes:
            individualVol = 0
            individualUni = 0
            loacalPerVolDict[volume.htid] = {}
            per_vol_set[volume.htid] = {}

            body = volume.features.body
            if body is not None:
                update_dict(body, loacalPerVolDict[volume.htid])
                updatedset(body, per_vol_set[volume.htid], volume.htid)

            total += volume.features.token_count
            individualVol = volume.features.token_count

            volumeId = volume.htid

            individualUni = ((len(per_vol_set[volumeId][volumeId]) if volumeId in per_vol_set[volumeId] else 0) if volumeId in per_vol_set else 0)

            totalunique += individualUni

            """if (!document_lengths[volume.metadata.title] || typeof document_lengths[volume.metadata.title] !== 'object') {
            document_lengths[volume.metadata.title] = {};
            }"""
            document_lengths[volume.metadata.id] = { 'title': volume.metadata.title, 'value': individualVol}

            document_words[volume.metadata.id] = { 'title': volume.metadata.title, 'value': individualVol}
    
            vocab_density[volume.metadata.id] = { 'title': volume.metadata.title, 'value': ((individualVol / individualUni) if individualUni > 0 else 0) / 100 }
        
            #read_score = calculate_readability(individualVol)
            #readability_score[volume.metadata.title] = read_score;
        print("get_data summary B")
        output_data = { 'worksetSize': len(volumes), 'totalWords': total, 'uniqueWords': totalunique, 'lengthGraph': document_lengths, 'densityGraph': vocab_density }
        print("get_data summary C")
        # Find the longest document
        longestDocumentsString = find_extreme_value(document_lengths,'max')
        output_data['longestDoc'] = longestDocumentsString
        print("get_data summary D")
        # Find the shortest document
        shortestDocumentsString = find_extreme_value(document_lengths,'min')
        output_data['shortestDoc'] = shortestDocumentsString
        print("get_data summary E")
        # Find the document with the highest vocabulary density
        highestDense = find_extreme_value(vocab_density,'max')
        output_data['highestDensityDoc'] = highestDense
        print("get_data summary F")
        # Find the document with the lowest vocabulary density
        lowestDense = find_extreme_value(vocab_density,'min')
        output_data['lowestDensityDoc'] = lowestDense
        print("get_data summary G")
        """ // Find the document with the highest readability score
        const highestReadabilityDocument = Object.keys(readability_score).reduce((a, b) => readability_score[a] > readabilityScore[b] ? a : b);
        const highestReadability = readability_score[highestReadabilityDocument];

        // Find the document with the lowest readability score
        const lowestReadabilityDocument = Object.keys(readability_score).reduce((a, b) => readability_score[a] < readabilityScore[b] ? a : b);
        const lowestReadability = readability_score[lowestReadabilityDocument];"""

        # Check the type
        return output_data
