# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mercylog', 'mercylog.config', 'mercylog.lib']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses>=0.6.0,<0.7.0',
 'multipledispatch>=0.6.0,<0.7.0',
 'mypy>=0.720.0,<0.721.0',
 'toolz>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'mercylog',
    'version': '0.1.0',
    'description': 'Datalog Inspired Logic Programming in Python',
    'long_description': None,
    'author': 'Rajiv Abraham',
    'author_email': 'rajiv.abraham@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
