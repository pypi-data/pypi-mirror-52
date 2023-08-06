# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['fluency']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fluency',
    'version': '0.1.0',
    'description': 'Get sentence-level fluency scores.',
    'long_description': None,
    'author': 'Motoki Wu',
    'author_email': 'tokestermw@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
