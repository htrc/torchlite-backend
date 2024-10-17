import nltk
from .converters import torchlite_volume_meta_from_ef
from .ef.models import Volume
from .models.dashboard import FilterSettings
from .models.dashboard import DataCleaningSettings
from .utils import make_set
from nltk.corpus import stopwords
import os
import json
import regex as re

def apply_filters(volumes: list[Volume], filters: FilterSettings) -> list[Volume]:
    filtered_volumes = []
    for volume in volumes:
        volume_meta = torchlite_volume_meta_from_ef(volume)
        if filters.titles and volume_meta.title not in filters.titles:
            continue
        if filters.pub_dates and volume_meta.pub_date not in filters.pub_dates:
            continue
        if filters.genres and not make_set(volume_meta.genre).intersection(filters.genres):
            continue
        if filters.type_of_resources and volume_meta.type_of_resource not in filters.type_of_resources:
            continue
        if filters.categories and not make_set(volume_meta.category).intersection(filters.categories):
            continue
        if filters.contributors and not make_set(volume_meta.contributor).intersection(filters.contributors):
            continue
        if filters.publishers and not make_set(volume_meta.publisher).intersection(filters.publishers):
            continue
        if filters.access_rights and volume_meta.access_rights not in filters.access_rights:
            continue
        if filters.pub_places and not make_set(volume_meta.pub_place).intersection(filters.pub_places):
            continue
        if filters.languages and not make_set(volume_meta.language).intersection(filters.languages):
            continue
        if filters.source_institutions and volume_meta.source_institution not in filters.source_institutions:
            continue

        filtered_volumes.append(volume)

    return filtered_volumes

def load_stopwords(language, directory="stopword_lists"):
    #COMMON CODE, SHOULD BE CALLED ONCE
    default_languages = ['english', 'german', 'spanish', 'french']
    if not os.path.exists(directory):
        os.makedirs(directory)
    for lang in default_languages:
        stopword_list = stopwords.words(lang)
        stopword_file_path = os.path.join(directory, f"{lang}_stopwords.json")
        with open(stopword_file_path, 'w', encoding='utf-8') as file:
            json.dump(stopword_list, file, ensure_ascii=False, indent=4)
    ######

    stopword_file_path = os.path.join(directory, f"{language}_stopwords.json")

    if not os.path.exists(stopword_file_path):
        print(f"Stopwords file for language '{language}' not found.")

    with open(stopword_file_path, 'r', encoding='utf-8') as file:
        stopword_list = json.load(file)
    
    return stopword_list

def clean_volume_data(volume, stopwords, regex_pattern):
    cleaned_data = {}

    for word, count in volume['features']['body'].items():
        lower_word = word.lower()

        if lower_word not in stopwords and not re.search(regex_pattern, lower_word):
            cleaned_data[lower_word] = count

    return {
        **volume,
        'features': {
            **volume['features'],
            'body': cleaned_data
        }
    }

def apply_datacleaning(filtered_volumes, cleaning_settings: DataCleaningSettings):
    language = cleaning_settings.get('language', 'english')
    
    stopwords = load_stopwords(language)
    regex_pattern = re.compile(r'[\p{P}\d]')

    cleaned_volumes = []
    for volume in filtered_volumes:
        cleaned_volume = clean_volume_data(volume, stopwords, regex_pattern) 
        cleaned_volumes.append(cleaned_volume)

    return cleaned_volumes

#new language list can be loaded when selected