from uuid import UUID

import nltk 
from .converters import torchlite_volume_meta_from_ef
from .ef.models import Volume
from .models.dashboard import FilterSettings
from .models.dashboard import DataCleaningSettings
from .utils import make_set
from .config import config
from nltk.corpus import stopwords
import os
import json
import logging

log = logging.getLogger(config.PROJECT_NAME)

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

def load_stopwords(dashboard_id: UUID, language: str, directory="stopword_lists"):
    nltk.download('stopwords')
    default_languages = ['english', 'german', 'spanish', 'french']
    if not os.path.exists(directory):
        os.makedirs(directory)
    for lang in default_languages:
        stopword_list = stopwords.words(lang)
        stopword_file_path = os.path.join(directory, f"{lang}_stopwords.json")
        with open(stopword_file_path, 'w', encoding='utf-8') as file:
            json.dump(stopword_list, file, ensure_ascii=False, indent=4)

    stopword_file_path = os.path.join(directory, f"{dashboard_id}_stopwords.json")
    log.debug(stopword_file_path)
    log.debug(os.path.exists(stopword_file_path))
    if lang not in ["English", "German", "French", "Spanish"]:
        if (os.path.exists(stopword_file_path)):
            with open(stopword_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)

    default_stopword_file = os.path.join(directory, f"{language}_stopwords.json")
    if (os.path.exists(default_stopword_file)):
        with open(default_stopword_file, 'r', encoding='utf-8') as file:
            return json.load(file)

def clean_volume_data(volume: Volume, stopwords: list[str]):
    cleaned_data = {}

    for word, count in volume.features.body.items():
        lower_word = word.lower()

        if lower_word not in stopwords:
            if lower_word not in cleaned_data:
                cleaned_data[lower_word] = count
            else:
                cleaned_data[lower_word] += count
    volume.features.body = cleaned_data
    return volume

def apply_datacleaning(dashboard_id: UUID, filtered_volumes: list[Volume], cleaning_settings: DataCleaningSettings):
    
    language = cleaning_settings.language 
    
    cleaned_volumes = []
    if (language):
        stopwords = load_stopwords(dashboard_id, language.lower())
    
        count = 0
        for volume in filtered_volumes:
            log.debug(f"'me' present before cleaning: {'me' in volume.features.body}")
            cleaned_volume = clean_volume_data(volume, stopwords) 
            count += 1
            log.debug(f"'me' present after cleaning: {'me' in cleaned_volume.features.body}")
            cleaned_volumes.append(cleaned_volume)

        return cleaned_volumes
    return filtered_volumes