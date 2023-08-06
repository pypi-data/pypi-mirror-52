# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['envtoml']

package_data = \
{'': ['*']}

install_requires = \
['coverage>=4.5,<5.0', 'nose>=1.3,<2.0', 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'envtoml',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'mr.Shu',
    'author_email': 'mr@shu.io',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
