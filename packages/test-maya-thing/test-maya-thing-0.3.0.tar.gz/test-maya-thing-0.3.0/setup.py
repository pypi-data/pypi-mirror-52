# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['testmayathing']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'test-maya-thing',
    'version': '0.3.0',
    'description': 'Maya Boilerplate contains all the boilerplate you need to create a Maya Python package.',
    'long_description': None,
    'author': 'Mitchell Coote',
    'author_email': 'mitchellcoote@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
