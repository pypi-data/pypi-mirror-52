# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['django_handyman']

package_data = \
{'': ['*']}

install_requires = \
['codecov>=2.0,<3.0']

setup_kwargs = {
    'name': 'django-handyman',
    'version': '1.0.0rc1',
    'description': '',
    'long_description': None,
    'author': 'Giannis Katsini',
    'author_email': 'giannis.katsini@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
