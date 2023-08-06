# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['json_schema_discovery']

package_data = \
{'': ['*']}

install_requires = \
['tabulate>=0.8.3,<0.9.0']

setup_kwargs = {
    'name': 'json-schema-discovery',
    'version': '1.3.2',
    'description': 'Database-agnostic JSON schema discovery',
    'long_description': 'Database-agnostic JSON schema discovery\n\nQuickly get insight into the general structure of a large set of JSON files by creating a structure summary showing the type and frequency of objects key\n\n\nQuickstart\n----------\n\nStart with ``Empty`` or by passing a python object to ``make_schema()``\n\nMerge a schema onto another using ``+=`` (also accepts python objects on the right hand side)\n\nVisualize the resulting schema with ``dumps()`` or by printing the object\n\nGet a detailed tabulated view of the overall structure with ``statistics()``\n',
    'author': 'Stepland',
    'author_email': 'Stepland@hotmail.fr',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
