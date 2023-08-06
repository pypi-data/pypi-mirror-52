# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cruft']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cruft',
    'version': '0.0.1',
    'description': 'Allows you to maintain all the necessary cruft for packaging and building projects separate from the code you intentionally write. Built on-top of CookieCutter.',
    'long_description': 'cruft\n_________________\n\n[![PyPI version](https://badge.fury.io/py/cruft.svg)](http://badge.fury.io/py/cruft)\n[![Build Status](https://travis-ci.org/timothycrosley/cruft.svg?branch=master)](https://travis-ci.org/timothycrosley/cruft)\n[![codecov](https://codecov.io/gh/timothycrosley/cruft/branch/master/graph/badge.svg)](https://codecov.io/gh/timothycrosley/cruft)\n[![Join the chat at https://gitter.im/timothycrosley/cruft](https://badges.gitter.im/timothycrosley/cruft.svg)](https://gitter.im/timothycrosley/cruft?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/cruft/)\n[![Downloads](https://pepy.tech/badge/cruft)](https://pepy.tech/project/cruft)\n_________________\n\n[Read Latest Documentation](https://timothycrosley.github.io/cruft/) - [Browse GitHub Code Repository](https://github.com/timothycrosley/cruft/)\n_________________\n\n**cruft** Allows you to maintain all the necessary cruft for packaging and building projects separate from the code you intentionally write. Built on-top of CookieCutter.\n',
    'author': 'Timothy Crosley',
    'author_email': 'timothy.crosley@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
