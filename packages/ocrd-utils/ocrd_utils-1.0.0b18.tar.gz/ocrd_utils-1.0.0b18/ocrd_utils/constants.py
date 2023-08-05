"""
Constants for ocrd_utils.
"""
from pkg_resources import get_distribution

__all__ = [
    'VERSION',
    'MIMETYPE_PAGE',
    'EXT_TO_MIME',
    'MIME_TO_EXT'
]

VERSION = get_distribution('ocrd_utils').version

MIMETYPE_PAGE = 'application/vnd.prima.page+xml'

EXT_TO_MIME = {
    '.tif': 'image/tiff',
    '.tiff': 'image/tiff',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.jpeg': 'image/jpg',
    '.xml': MIMETYPE_PAGE
}

MIME_TO_EXT = {
    'image/tiff': '.tif',
    'image/png': '.png',
    'image/jpg': '.jpg',
    'image/jpeg': '.jpg',
    MIMETYPE_PAGE: '.xml',
    'application/alto+xml': '.xml',
}
