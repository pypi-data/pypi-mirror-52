# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ipy_pdcache']

package_data = \
{'': ['*'], 'ipy_pdcache': ['tests/*']}

install_requires = \
['ipython>=7.8,<8.0', 'pandas>=0.25.1,<0.26.0']

setup_kwargs = {
    'name': 'ipy-pdcache',
    'version': '0.0.1',
    'description': 'Automatically cache results of intensive computations in IPython.',
    'long_description': None,
    'author': 'kpj',
    'author_email': 'kpjkpjkpjkpjkpjkpj@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
