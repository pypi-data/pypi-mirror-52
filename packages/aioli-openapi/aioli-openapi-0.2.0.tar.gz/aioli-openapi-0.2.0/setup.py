# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aioli_openapi']

package_data = \
{'': ['*']}

install_requires = \
['aioli>=0.5.0,<0.6.0', 'apispec>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'aioli-openapi',
    'version': '0.2.0',
    'description': 'Generate OpenAPI schemas using Aioli Handlers',
    'long_description': '',
    'author': 'Robert Wikman',
    'author_email': 'rbw@vault13.org',
    'url': 'https://github.com/aioli-framework/aioli-openapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
