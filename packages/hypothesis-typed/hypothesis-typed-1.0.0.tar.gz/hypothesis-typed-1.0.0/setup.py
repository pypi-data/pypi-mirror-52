# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hypothesis_typed']

package_data = \
{'': ['*']}

install_requires = \
['hypothesis_auto>=1.0,<2.0']

setup_kwargs = {
    'name': 'hypothesis-typed',
    'version': '1.0.0',
    'description': 'An alias for hypothesis-auto',
    'long_description': 'An alias for the [hypothesis-auto](https://timothycrosley.github.io/hypothesis-auto/) project.\n',
    'author': 'Timothy Crosley',
    'author_email': 'timothy.crosley@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
