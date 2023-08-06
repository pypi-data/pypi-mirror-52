# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['nimi']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9,<2.0',
 'click>=7.0,<8.0',
 'jinja2>=2.10,<3.0',
 'requests>=2.22,<3.0',
 'terminaltables>=3.1,<4.0']

entry_points = \
{'console_scripts': ['nimi = nimi:cli.cli']}

setup_kwargs = {
    'name': 'nimi',
    'version': '0.1.0',
    'description': 'Dynamic DNS on AWS',
    'long_description': None,
    'author': 'Martin Raag',
    'author_email': 'hi@mraag.xyz',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
