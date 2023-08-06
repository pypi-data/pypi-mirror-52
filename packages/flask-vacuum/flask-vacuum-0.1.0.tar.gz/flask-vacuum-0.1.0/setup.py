# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['flask_vacuum']

package_data = \
{'': ['*']}

install_requires = \
['flask-injector>=0.12.0,<0.13.0', 'flask>=1.1,<2.0']

setup_kwargs = {
    'name': 'flask-vacuum',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Anton Ruhlov',
    'author_email': 'antonruhlov@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
