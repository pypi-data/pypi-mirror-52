# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['square']

package_data = \
{'': ['*']}

install_requires = \
['bumpversion>=0.5.3,<0.6.0',
 'colorama>=0.4.1,<0.5.0',
 'flake8-isort>=2.7,<3.0',
 'flake8>=3.7,<4.0',
 'google-api-python-client>=1.7,<2.0',
 'google>=2.0,<3.0',
 'ipython>=7.8,<8.0',
 'isort>=4.3,<5.0',
 'jsonpatch>=1.24,<2.0',
 'pytest-cov>=2.7,<3.0',
 'pytest-dotenv>=0.4.0,<0.5.0',
 'pytest-flake8>=1.0,<2.0',
 'pyyaml>=5.1,<6.0',
 'requests-mock>=1.7,<2.0',
 'requests>=2.22,<3.0']

entry_points = \
{'console_scripts': ['square = square.square:main']}

setup_kwargs = {
    'name': 'kubernetes-square',
    'version': '0.11.0',
    'description': '',
    'long_description': None,
    'author': 'Oliver Nagy',
    'author_email': 'olitheolix@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
