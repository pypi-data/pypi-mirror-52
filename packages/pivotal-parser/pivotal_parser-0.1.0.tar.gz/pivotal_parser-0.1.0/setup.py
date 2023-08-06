# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pivotal_parser']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'pandas>=0.25.1,<0.26.0']

entry_points = \
{'console_scripts': ['pivotal_parser = pivotal_parser:cli.run']}

setup_kwargs = {
    'name': 'pivotal-parser',
    'version': '0.1.0',
    'description': 'Tool to parse out Pivotal Tracker CSVs.',
    'long_description': None,
    'author': 'Adam Drewery',
    'author_email': 'adam@verypossible.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
