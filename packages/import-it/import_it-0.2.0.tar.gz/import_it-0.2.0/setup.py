# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['import_it']

package_data = \
{'': ['*']}

install_requires = \
['ripgrepy>=1.0,<2.0']

entry_points = \
{'console_scripts': ['import_it.py = import_it:main']}

setup_kwargs = {
    'name': 'import-it',
    'version': '0.2.0',
    'description': 'Determine the way to import a symbol using rg.',
    'long_description': None,
    'author': 'Razzi Abuissa',
    'author_email': 'razzi@abuissa.net',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
