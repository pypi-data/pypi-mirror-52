# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['swashbookler']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1,<6.0',
 'bs4>=0.0.1,<0.0.2',
 'click>=7.0,<8.0',
 'img2pdf>=0.3.3,<0.4.0',
 'pillow>=6.1,<7.0',
 'requests>=2.22,<3.0']

entry_points = \
{'console_scripts': ['swashbookler = swashbookler.cli:cli']}

setup_kwargs = {
    'name': 'swashbookler',
    'version': '1.0.1',
    'description': 'Allows downloading books from Google Books and converting them to PDFs.',
    'long_description': None,
    'author': 'Coriander Pines',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
