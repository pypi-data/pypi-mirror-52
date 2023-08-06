# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': '.'}

packages = \
['loggable']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.14.3,<0.15.0', 'colorlog>=4.0,<5.0', 'tqdm>=4.32,<5.0']

setup_kwargs = {
    'name': 'loggable-jdv',
    'version': '0.1.5',
    'description': 'Logging package. Alpha. Not meant for wider release.',
    'long_description': None,
    'author': 'jvrana',
    'author_email': 'justin.vrana@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
