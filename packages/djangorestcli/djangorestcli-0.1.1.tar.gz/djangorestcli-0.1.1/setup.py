# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['djangorestcli', 'djangorestcli.controllers']

package_data = \
{'': ['*'], 'djangorestcli': ['templates/*']}

install_requires = \
['argparse>=1.4,<2.0']

setup_kwargs = {
    'name': 'djangorestcli',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Ronnasayd Machado',
    'author_email': 'ronnasayd@hotmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.7.*, !=3.8.*',
}


setup(**setup_kwargs)
