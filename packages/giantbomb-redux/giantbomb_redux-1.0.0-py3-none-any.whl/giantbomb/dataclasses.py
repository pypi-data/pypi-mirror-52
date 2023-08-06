from typing import List, Optional, Union
from dataclasses import dataclass


@dataclass
class Image:
    icon_url: Optional[str] = ''
    medium_url: Optional[str] = ''
    tiny_url: Optional[str] = ''
    small_url: Optional[str] = ''
    thumb_url: Optional[str] = ''
    screen_url: Optional[str] = ''
    super_url: Optional[str] = ''


@dataclass
class Platform:
    id: int
    name: str = ''
    abbreviation: Optional[str] = ''
    deck: Optional[str] = ''
    api_detail_url: Optional[str] = ''
    image: Optional[Image] = None
    install_base: Optional[str] = ''
    release_date: Optional[str] = ''
    description: Optional[str] = ''


@dataclass
class Region:
    id: int
    name: str = ''
    api_detail_url: str = ''


@dataclass
class Release:
    id: int
    name: str = ''
    deck: Optional[str] = ''
    region: Optional[Region] = None
    developers: Optional[List[str]] = ''
    site_detail_url: Optional[str] = ''
    api_detail_url: Optional[str] = ''


@dataclass
class Game:
    id: int = None
    name: str = ''
    deck: Optional[str] = ''
    platforms: Optional[List[Platform]] = None
    developers: Optional[list] = None
    publishers: Optional[list] = None
    franchises: Optional[list] = None
    releases: Optional[List[Union[Release, None]]] = None
    images: Optional[List[Union[Image, None]]] = None
    image: Image = None
    genres: Optional[list] = None
    original_release_date: Optional[str] = ''
    videos: Optional[list] = None
    api_detail_url: Optional[str] = ''
    site_detail_url: Optional[str] = ''
    date_added_gb: Optional[str] = ''
    date_last_updated_gb: Optional[str] = ''


@dataclass
class Franchise:
    id: int
    name: Optional[str] = ''
    deck: Optional[str] = ''
    api_detail_url: Optional[str] = ''
    image: Image = None


@dataclass
class Genre:
    id: int
    name: Optional[str] = ''
    api_detail_url: Optional[str] = ''


@dataclass
class Videos:
    id: int
    name: Optional[str] = ''
    deck: Optional[str] = ''
    image: Image = None
    url: Optional[str] = ''
    publish_date: Optional[str] = ''


@dataclass
class Video:
    id: id
    name: Optional[str] = ''
    deck: Optional[str] = ''
    image: Image = None
    url: Optional[str] = ''
    publish_date: Optional[str] = ''
    site_detail_url: Optional[str] = ''


@dataclass
class SearchResult:
    id: int = ''
    name: Optional[str] = ''
    api_detail_url: Optional[str] = ''
    image: Image = None
