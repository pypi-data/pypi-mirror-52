# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['attrs_marshmallow']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'attrs-marshmallow',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Igor Stuzhuk (KoHcoJlb)',
    'author_email': 'fujitsuigor@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
