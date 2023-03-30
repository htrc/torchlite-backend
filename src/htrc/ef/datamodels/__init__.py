from typing import Any, List, Union
from pydantic import BaseModel, ValidationError, DateTimeError

class Workset(BaseModel):
    id: str
    htids: List[str]
    created: str


class Contributor(BaseModel):
    id: str
    type: str
    name: str


class Publisher(BaseModel):
    id: str
    type: str
    name: str


class PublicationPlace(BaseModel):
    id: Union[str, None]
    type: Union[str, None]
    name: Union[str, None]


class SourceInstitution(BaseModel):
    type: str
    name: str


class Journal(BaseModel):
    id: str
    type: str
    journalTitle: str


class VolumeMetadata(BaseModel):
    schemaVersion: Union[str, None]
    id: Union[str, None]
    type: Union[List[str], None]
    dateCreated: Union[int, None]
    title: Union[str, None]
    alternateTitle: Union[str, List[str], None]
    enumerationChronology: Union[str, None]
    contributor: Union[Contributor, List[Contributor], None]
    pubDate: Union[int, None]
    publisher: Union[Publisher, List[Publisher], None]
    pubPlace: Union[PublicationPlace, List[PublicationPlace], None]
    language: Union[str, List[str], None]
    accessRights: Union[str, None]
    accessProfile: Union[str, None]
    sourceInstitution: Union[SourceInstitution, None]
    mainEntityOfPage: Union[List[str], None]
    lcc: Union[str, List[str], None]
    oclc: Union[str, List[str], None]
    issn: Union[str, List[str], None]
    isbn: Union[str, List[str], None]
    category: Union[str, List[str], None]
    genre: Union[str, List[str], None]
    typeOfResource: Union[str, None]
    lastRightsUpateDate: Union[int, None]
    isPartOf: Union[Journal, None]


class Volume(BaseModel):
    htid: str
    metadata: VolumeMetadata

    def __repr__(self):
        return f"Volume({self.htid})"
