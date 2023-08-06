# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ugoira']

package_data = \
{'': ['*']}

install_requires = \
['Wand>=0.5.7,<0.6.0', 'click>=7.0,<8.0', 'fake_useragent>=0.1.11,<0.2.0']

extras_require = \
{'apng': ['apng>=0.3.3,<0.4.0']}

entry_points = \
{'console_scripts': ['ugoira = ugoira.cli:ugoira']}

setup_kwargs = {
    'name': 'ugoira',
    'version': '0.6.0',
    'description': 'ugoira for download pixiv ugoira images',
    'long_description': None,
    'author': 'Kim Jin Su',
    'author_email': 'item4_hun@hotmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
