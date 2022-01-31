from dataclasses import dataclass
from typing import List


@dataclass
class Metadata:
    date: str
    client_name: str
    location: str


@dataclass
class SectionData:
    number: str
    title: str
    score: float
    scope: str


@dataclass
class SubsectionData():
    number: str
    title: str
    comments: str
    score: float


@dataclass
class Section():
    section_data: SectionData
    subsections_data: List[SubsectionData]


@dataclass
class DataItem:
    metadata: Metadata
    sectionDataList: List[SectionData]
    subsectionDataList: List[SubsectionData]
