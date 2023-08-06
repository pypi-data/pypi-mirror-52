# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['altair_recipes']

package_data = \
{'': ['*']}

install_requires = \
['altair>=3.2.0',
 'autosig>=0.7.0',
 'boltons>=19.1.0',
 'numpy>=1.17.0',
 'pandas>=0.25.0',
 'requests>=2.22.0',
 'toolz>=0.10.0']

setup_kwargs = {
    'name': 'altair-recipes',
    'version': '0.6.2',
    'description': 'A collection of ready-made statistical graphics for vega',
    'long_description': None,
    'author': 'Antonio Piccolboni',
    'author_email': 'antonio@piccolboni.info',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
