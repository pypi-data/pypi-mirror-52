# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['sushi_allergy_parser']

package_data = \
{'': ['*']}

install_requires = \
['tabula-py>=1.4,<2.0']

setup_kwargs = {
    'name': 'sushi-allergy-parser',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 't3yamoto',
    'author_email': '3yamoto.dev@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
