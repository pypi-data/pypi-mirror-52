# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fastjsonrpc']

package_data = \
{'': ['*']}

install_requires = \
['Twisted>=19.7,<20.0', 'pyOpenSSL>=19.0,<20.0']

setup_kwargs = {
    'name': 'quickjsonrpc',
    'version': '0.4.0',
    'description': 'A library for writing asynchronous JSON-RPC servers and clients in Python, using Twisted',
    'long_description': None,
    'author': 'Daniel Gonzalez',
    'author_email': 'gonvaled@gonvaled.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
