# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['django_handyman', 'django_handyman.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-handyman',
    'version': '1.0.1',
    'description': '',
    'long_description': None,
    'author': 'Giannis Katsini',
    'author_email': 'giannis.katsini@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
