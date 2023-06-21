from pydantic import BaseModel
from typing import Optional, Sequence, Union, NamedTuple


class Contributor(BaseModel):
    id: str
    type: str
    name: str


class Publisher(BaseModel):
    id: str
    type: str
    name: str


class PublicationPlace(BaseModel):
    id: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None


class SourceInstitution(BaseModel):
    type: str
    name: str


class Journal(BaseModel):
    id: str
    type: str
    journalTitle: str


class CharCount(NamedTuple):
    char: str
    cnt: int


class PosCount(BaseModel):
    pos: str
    cnt: int


class TokenCount(BaseModel):
    tok: str
    cnt: int


class TokenPosCount(BaseModel):
    tok: str
    posCnts: Sequence[PosCount]


class VolumeMetadata(BaseModel):
    schemaVersion: Optional[str] = None
    id: Optional[str] = None
    type: Optional[Sequence[str]] = None
    dateCreated: Optional[int] = None
    title: Optional[str] = None
    alternateTitle: Optional[Union[str, list[str]]] = None
    enumerationChronology: Optional[str] = None
    contributor: Optional[Union[Contributor, list[Contributor]]] = None
    pubDate: Optional[int] = None
    publisher: Optional[Union[Publisher, list[Publisher]]] = None
    pubPlace: Optional[Union[PublicationPlace, list[PublicationPlace]]] = None
    language: Optional[Union[str, list[str]]] = None
    accessRights: Optional[str] = None
    accessProfile: Optional[str] = None
    sourceInstitution: Optional[SourceInstitution] = None
    mainEntityOfPage: Optional[Sequence[str]] = None
    lcc: Optional[Union[str, Sequence[str]]] = None
    oclc: Optional[Union[str, Sequence[str]]] = None
    issn: Optional[Union[str, Sequence[str]]] = None
    isbn: Optional[Union[str, Sequence[str]]] = None
    category: Optional[Union[str, Sequence[str]]] = None
    genre: Optional[Union[str, Sequence[str]]] = None
    typeOfResource: Optional[str] = None
    lastRightsUpateDate: Optional[int] = None
    isPartOf: Optional[Journal] = None


class PosSectionFeatures(BaseModel):
    tokenCount: Optional[int] = None
    lineCount: Optional[int] = None
    emptyLineCount: Optional[int] = None
    sentenceCount: Optional[int] = None
    capAlphaSeq: Optional[int] = None
    beginCharCount: dict[str, int] | None = None
    endCharCount: dict[str, int] | None = None
    tokenPosCount: dict | None = None


class SectionFeatures(BaseModel):
    tokenCount: Optional[int] = None
    lineCount: Optional[int] = None
    emptyLineCount: Optional[int] = None
    sentenceCount: Optional[int] = None
    capAlphaSeq: Optional[int] = None
    beginCharCount: dict[str, int] | None = None
    endCharCount: dict[str, int] | None = None
    tokensCount: dict | None = None


class PageFeatures(BaseModel):
    seq: Optional[str] = None
    version: Optional[str] = None
    tokenCount: Optional[int] = None
    lineCount: Optional[int] = None
    emptyLineCount: Optional[int] = None
    sentenceCount: Optional[int] = None
    header: PosSectionFeatures | SectionFeatures | None = None
    body: PosSectionFeatures | SectionFeatures | None = None
    footer: PosSectionFeatures | SectionFeatures | None = None
    calculatedLanguage: Optional[str] = None


class VolumeFeatures(BaseModel):
    type: Optional[str] = None
    id: Optional[str] = None
    schemaVersion: Optional[str] = None
    dateCreated: Optional[int] = None
    pageCount: Optional[int] = None
    pages: Optional[Sequence[PageFeatures]] = []


class EF(BaseModel):
    context: Optional[str] = None
    schemaVersion: Optional[str] = None
    id: Optional[str] = None
    htid: Optional[str] = None
    type: Optional[str] = None
    publisher: Optional[Publisher]
    datePublished: Optional[int] = None
    metadata: Optional[VolumeMetadata] = None
    features: Optional[VolumeFeatures] = None


class Workset(BaseModel):
    id: str
    htids: list[str]
    created: str


class Volume(BaseModel):
    htid: str
    metadata: Optional[VolumeMetadata] = None
