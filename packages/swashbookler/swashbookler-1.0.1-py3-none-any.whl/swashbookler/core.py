import os
import random
import re
import requests
import multiprocessing
import multiprocessing.pool
from typing import Optional, Dict, List
import unicodedata
import yaml
from bs4 import BeautifulSoup
import img2pdf
import shutil
import logging
import time

__all__ = [
    'download_book'
]

_PAGE_URL: str = 'https://books.google.com/books?id={book_id}&jtp={page}'

_USER_AGENTS: List[str] = [
    'Mozilla/5.0 (Mobile; rv:18.0) Gecko/18.0 Firefox/18.0',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; MSAppHost/1.0)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10B142',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
]

_MAX_DOWNLOAD_ATTEMPTS = 5

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def download_book(
        book_id: str,
        fetch_metadata: bool = True,
        save_pdf: bool = True,
        save_images: bool = False,
        width: int = 2048,
        max_threads: Optional[int] = None,
        max_pages: Optional[int] = None):
    """Downloads a Google book with a given ID.

    :param book_id: The ID of the book to download
    :param fetch_metadata: If True, get additional metadata and save it into a companion file
    :param save_pdf: If True, download book as a PDF. Default True.
    :param save_images: If True, download pages as individual images. Default False.
    :param width: The page image width in pixels. Default 2048.
    :param max_threads: The maximum number of download threads to use, or None to default to the number of CPUs
    :param max_pages: If specified, only this number of pages will be downloaded. Default None, for all pages
    """

    book_url = _PAGE_URL.format(book_id=book_id, page=0)
    log.info('Downloading book at %s', book_url)
    start_time = time.time()

    # Grab metadata
    metadata = {'title': book_id}
    if fetch_metadata:
        log.debug('Fetching metadata...')
        try:
            metadata = _get_metadata(book_url)
        except requests.RequestException as e:
            log.warning(
                'Failed to download metadata. Check that book ID is valid and network is available. Error: %s', str(e))
        except Exception as e:
            log.warning('Failed to parse metadata: %s', str(e))

    book_filename = _slugify(metadata['title'])
    directory_filename = _slugify('{}_images'.format(book_id))
    log.info('Saving book as \"%s\"', book_filename)

    # Download metadata
    if fetch_metadata:
        with open('{}.yaml'.format(book_filename), 'w') as metadata_file:
            yaml.dump(metadata, metadata_file)

    if not save_pdf and not save_images:
        return

    # Create directory to hold downloaded files
    os.makedirs(directory_filename, exist_ok=True)

    # Find pages and download them
    log.debug('Getting page info and downloading images...')
    try:
        page_filenames = _discover_and_save_pages(book_url, width, max_pages, directory_filename, max_threads)
    except requests.RequestException:
        log.error('Failed to download book pages. Check that book ID is valid and network is available.')
        raise
    except Exception as e:
        log.error('Failed to parse page info: %s', str(e))
        raise

    # Assemble to PDF
    if save_pdf:
        log.debug('Saving PDF...')
        with open('{}.pdf'.format(book_filename), 'wb') as pdf_file:
            pdf_file.write(img2pdf.convert(page_filenames))
        log.info('Book PDF saved')

    # Delete images if not needed
    if save_images:
        log.debug('Saving page images to output directory...')
        os.makedirs(book_filename, exist_ok=True)
        for page_filename in page_filenames:
            shutil.copy(page_filename, book_filename)
        log.info('Saved page images to output directory')

    log.debug('Deleting temporary files...')
    for page_filename in page_filenames:
        try:
            os.remove(page_filename)
        except OSError as e:
            log.error('Could not remove temporary file \"%s\", got error: %s', page_filename, str(e))

    if os.path.exists(directory_filename) \
            and os.path.isdir(directory_filename) \
            and not os.listdir(directory_filename):
        os.rmdir(directory_filename)

    log.info('Removed temporary files')

    end_time = time.time()
    elapsed = end_time - start_time
    log.info('Downloaded book in %.1f seconds, at a rate of %.2f seconds per page', elapsed, elapsed / len(page_filenames))


def _slugify(text: str) -> str:
    """Removes invalid characters from a string, rendering it usable as a filename.

    :param text: Input string, supporting Unicode
    :returns: A normalized string with whitespace and invalid characters replaced with hyphens.
    """

    text = unicodedata.normalize('NFKD', text)
    text = re.sub(r'[^\w\s-]', '', text).strip()
    return re.sub(r'[-\s]+', '-', text)


def _get_remote_file(url: str, attempts: Optional[int] = None) -> requests.Response:
    """Fetches a remote file at a given URL. Automatically reties if the file could not be downloaded.

    :param url: The URL of the file to download
    :param attempts: The max number of attempts to allow. Default 5
    :returns: A "requests" Response with the contents of the file
    :raises requests.exceptions.RequestException: Raised by "requests" in the event of an error
    """

    if attempts is None:
        attempts = _MAX_DOWNLOAD_ATTEMPTS

    if attempts < 1:
        attempts = 1

    while True:
        attempts -= 1
        try:
            # NB: Google denies access if a browser-like user agent isn't supplied.
            # Randomizing the user-agent also tends to speed up downloading for some reason.
            headers = {
                'user-agent': random.choice(_USER_AGENTS)
            }

            req = requests.get(url, headers=headers)
            req.raise_for_status()
            log.debug('\t[%i] Downloaded file at %s', req.status_code, url)
            return req
        except requests.exceptions.RequestException as e:
            log.warning('Could not download %s. Remaining attempts: %i Error: %s', url, attempts, str(e))
            if attempts < 1:
                log.error('Failed to download %s', url)
                raise e


def _discover_and_save_pages(
        book_url: str, width: int, max_pages: Optional[int], directory: str, max_threads: Optional[int]) -> List[str]:
    """Assembles page information for a given book and downloads associated page images.
    Simultaneously locates pages and downloads images to save time.

    :param book_url: The URL for the book
    :param width: The suggested page image width in pixels. Google may not respect the exact dimensions.
    :param max_pages: The maximum pages to download, or None for all
    :param directory: Output directory for images
    :param max_threads: The maximum page download threads to use, or None for default. Use 0 to download in single-thread mode.
    :returns: A list of page filenames in order.
    """
    url = book_url
    first_page_code = None
    page_number = 0
    page_filenames = []

    # Set up pool if using
    pool = None
    if max_threads is not None and max_threads <= 0:
        log.debug('Downloading pages in single-threaded mode...')
    else:
        log.debug('Downloaded pages using %i processes...', max_threads or multiprocessing.cpu_count())
        pool = multiprocessing.pool.ThreadPool(processes=max_threads)

    log.debug('Getting page info...')
    while True:
        # Request the next page
        page = _get_remote_file(url)

        # Parse the page
        page_soup = BeautifulSoup(page.text, 'html.parser')

        # Extract image URL and page code from page style guide
        try:
            style = page_soup.find('div', class_='html_page_image').parent.style.text
            image_url = re.search(r'background-image:\s*url\(\s*"([^"]+)"\s*\)', style).group(1)
        except AttributeError as e:
            log.error('Could not parse page. Error: %s', str(e))
            raise e

        image_url = image_url + '&w={}'.format(width)  # Force a larger image size

        try:
            match = re.search(r'&pg=([^&]+)', image_url)
            page_code = match.group(1)
        except (AttributeError, IndexError) as e:
            log.error('Could not parse page. Error: %s', str(e))
            raise e

        log.info('Discovered page %i (%s)', page_number + 1, page_code)

        # Download the page
        page_filename = os.path.join(directory, '{}.png'.format(_slugify(page_code)))
        page_filenames.append(page_filename)

        page_name = '{page_number} ({page_code})'.format(page_number=page_number + 1, page_code=page_code)

        if pool:
            pool.apply_async(_download_and_save_page, args=(image_url, page_filename, page_name))
        else:
            _download_and_save_page(image_url, page_filename, page_name)

        # Extract URL and code for next page
        try:
            next_page = page_soup.find(id="next_btn").find_parent('a').get('href')
            next_page_code = re.search(r'&pg=([^&]+)', next_page).group(1)
        except (AttributeError, IndexError) as e:
            log.error('Could not parse page. Error: %s', str(e))
            raise e

        # Check that the next page isn't the first page (indicating the end of the book)
        if next_page_code == first_page_code:
            break

        # If this is the first page we've checked, extract the image code and store it to compare against
        if first_page_code is None:
            first_page_code = page_code

        # Move on to the next page
        url = next_page
        page_number += 1

        if max_pages is not None and page_number >= max_pages:
            break

    if pool:
        log.info('Page discovery complete')
        log.debug('Waiting for image downloads to complete...')
        pool.close()
        pool.join()
        log.info('Downloaded all pages')
    else:
        log.info('Page discovery and download complete')

    return page_filenames


def _get_metadata(book_url: str) -> Dict[str, str]:
    """Fetches metadata from a given book.

    :param book_url: The URL of the book to download
    :returns: A dictionary of book metadata
    """

    metadata = dict()

    # Download metadata from book URL
    first_page = _get_remote_file(book_url)
    first_page_soup = BeautifulSoup(first_page.text, 'html.parser')

    # Basic metadata
    try:
        metadata['title'] = first_page_soup.head.find('meta', attrs={'name': 'title'}).get('content')
    except AttributeError:
        pass

    try:
        metadata['description'] = first_page_soup.head.find('meta', attrs={'name': 'description'}).get('content')
    except AttributeError:
        pass

    try:
        metadata['about_url'] = first_page_soup.head.find('link', rel='canonical').get('href')
    except AttributeError:
        pass

    log.info('Got basic metadata')

    # Download "about" page, if possible
    if not metadata.get('about_url', None):
        log.warning('Could not locate extended metadata')
        return {k: v for k, v in metadata.items() if v is not None}

    try:
        about_page = _get_remote_file(metadata['about_url'])
        about_page_soup = BeautifulSoup(about_page.text, 'html.parser')

        # Additional metadata from "about" page
        try:
            metadata['full_title'] = about_page_soup.find(id='bookinfo').find(class_='booktitle').text
        except AttributeError:
            pass

        try:
            metadata['synopsis'] = about_page_soup.find(id='bookinfo').find(id='synopsis').text
        except AttributeError:
            pass

        try:
            infoblock = list(about_page_soup.find(id='bookinfo').find(class_="bookinfo_sectionwrap").children)

            metadata['author'] = infoblock[0].text
            pub_and_year, categories, pages_str = infoblock[1].text.split('-')
            metadata['categories'] = categories.strip()
            metadata['pages'] = pages_str.strip()
            publisher, year = pub_and_year.split(',')
            metadata['publisher'] = publisher.strip()
            metadata['year'] = year.strip()
        except (AttributeError, IndexError):
            pass

        log.info('Got extended metadata')
    except Exception as e:
        log.warning('Could not get extended metadata. Error: %s', str(e))

    return {k: v for k, v in metadata.items() if v is not None}


def _download_and_save_page(image_url: str, filename: str, page_name: Optional[str] = None):
    """Download a page and save it to a file.

    :param image_url: The URL of the page's image
    :param filename: THe local filename to which to save the page
    :param page_name: If specified, the name of the page to include in log messages
    """

    req = _get_remote_file(image_url)
    with open(filename, 'wb') as f:
        f.write(req.content)

    if page_name:
        log.info('Saved page %s to %s', page_name, filename)
    else:
        log.info('Saved page to %s')
