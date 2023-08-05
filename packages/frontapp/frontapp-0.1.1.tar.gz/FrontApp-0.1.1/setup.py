# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['frontapp']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.1,<20.0',
 'decorator>=4.4,<5.0',
 'envparse>=0.2.0,<0.3.0',
 'fastapi>=0.38.1,<0.39.0',
 'requests>=2.22,<3.0',
 'uvicorn>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'frontapp',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'MB',
    'author_email': 'mb@m1k.pw',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
