# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['import_it']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'import-it',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Razzi Abuissa',
    'author_email': 'razzi53@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
