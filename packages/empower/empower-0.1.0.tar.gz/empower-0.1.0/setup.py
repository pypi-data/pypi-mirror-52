# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['empower']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'empower',
    'version': '0.1.0',
    'description': 'Goodbye Inheritance',
    'long_description': None,
    'author': 'ZhengYu, Xu',
    'author_email': 'zen-xu@outlook.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
