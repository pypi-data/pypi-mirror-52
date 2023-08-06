# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['class_doc']
install_requires = \
['more-itertools>=7.2,<8.0']

setup_kwargs = {
    'name': 'class-doc',
    'version': '0.1.1',
    'description': 'Extract attributes docstrings defined in various ways',
    'long_description': '# Class doc\n\nSmall set of helpers aimed to extract class attributes documentation from a class definition, closely mimicking [sphinx-autodoc behaviour](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-autoattribute) (except instance attributes defined inside `__init__` function).\n\nThe main motivation for this project is undesirable integration of really heavy [sphinx-autodoc] dependency, also *sphinx* is usually used for development purposes. As opposite *class-doc* is light, serves a specific purpose and might be easily integrated in any project.\n\n## Installation\n\nThis package available on [PyPI]\n\n```bash\npip install class-doc\n```\n\nOr using [Poetry]\n\n```bash\npoetry add class-doc\n```\n\n## Examples\n\nShamely stolen from [sphinx-autodoc] docs\n\n```python\nclass Foo:\n    """Docstring for class Foo."""\n\n    #: Doc comment for class attribute Foo.bar.\n    #: It can have multiple lines.\n    bar = 1\n\n    flox = 1.5   #: Doc comment for Foo.flox. One line only.\n\n    baz = 2\n    """Docstring for class attribute Foo.baz."""\n\n\nimport class_doc\nassert class_doc.extract_docs_from_cls_obj(Foo) == {\n    "bar": ["Doc comment for class attribute Foo.bar.", "It can have multiple lines."],\n    "flox": ["Doc comment for Foo.flox. One line only."],\n    "baz": ["Docstring for class attribute Foo.baz."],\n}\n```\n\n## Development setup\n\nProject requires [Poetry] for development setup.\n\n* If you aren\'t have it already\n\n```sh\npip install poetry\n``` \n\n* Install project dependencies\n\n```sh\npoetry install\n```\n\n* Run tests\n\n```sh\npoetry run pytest .\n```\n\n* Great, all works!\n\n<!-- Links -->\n[PyPI]: http://pypi.org\n[Poetry]: https://poetry.eustace.io/\n[sphinx-autodoc]: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-autoattribute',
    'author': 'Daniel Daniels',
    'author_email': 'danields761@gmail.com',
    'url': 'https://github.com/danields761/class-doc',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
