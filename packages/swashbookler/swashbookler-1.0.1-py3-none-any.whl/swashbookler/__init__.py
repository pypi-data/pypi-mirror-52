"""Allows downloading books from Google Books and converting them to PDFs."""

from .core import download_book

__version__ = '1.0.1'

__all__ = [
    'download_book'
]
