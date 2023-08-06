# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['beetsplug']

package_data = \
{'': ['*']}

install_requires = \
['beets>=1.4,<2.0', 'confuse>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'beets-kergoth',
    'version': '0.2.0',
    'description': "Various personal beets plugins that don't yet have a home elsewhere.",
    'long_description': '',
    'author': 'Christopher Larson',
    'author_email': 'kergoth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kergoth/beets-kergoth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.8.*',
}


setup(**setup_kwargs)
