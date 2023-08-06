# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['make_help']

package_data = \
{'': ['*']}

install_requires = \
['click-pathlib>=2019.6.13,<2020.0.0', 'click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['make-help = make_help.cli:main']}

setup_kwargs = {
    'name': 'make-help',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Sam Bishop',
    'author_email': 'sam@techdragon.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
