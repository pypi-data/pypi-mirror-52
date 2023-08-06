# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['snmp_fetch', 'snmp_fetch.fp']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.1,<20.0',
 'numpy>=1.16,<2.0',
 'pandas>=0.25,<0.26',
 'toolz>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'snmp-fetch',
    'version': '0.1.0',
    'description': 'An opinionated python SNMPv2 library built for rapid database ingestion.',
    'long_description': None,
    'author': 'Christopher Aubut',
    'author_email': 'christopher@aubut.me',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
