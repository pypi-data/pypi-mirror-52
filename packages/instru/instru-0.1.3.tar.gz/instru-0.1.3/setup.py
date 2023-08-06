# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['instru']

package_data = \
{'': ['*']}

install_requires = \
['pymodbus>=2.2,<3.0', 'qcodes>=0.5.2,<0.6.0']

entry_points = \
{'console_scripts': ['demo = instru:main']}

setup_kwargs = {
    'name': 'instru',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'James Maxwell',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
