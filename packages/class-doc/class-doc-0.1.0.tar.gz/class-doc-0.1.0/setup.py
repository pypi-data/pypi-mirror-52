# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['class_doc']
install_requires = \
['more-itertools>=7.2,<8.0']

setup_kwargs = {
    'name': 'class-doc',
    'version': '0.1.0',
    'description': 'Extract attributes docstrings defined in various ways',
    'long_description': None,
    'author': 'Daniel Daniels',
    'author_email': 'danields761@gmail.com',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
