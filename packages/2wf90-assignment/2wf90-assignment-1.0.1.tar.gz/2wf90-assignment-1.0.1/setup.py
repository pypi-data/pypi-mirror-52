# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['2wf90_assignment']

package_data = \
{'': ['*'], '2wf90_assignment': ['unused/*']}

entry_points = \
{'console_scripts': ['2wf90 = 2wf90_assignment:entry']}

setup_kwargs = {
    'name': '2wf90-assignment',
    'version': '1.0.1',
    'description': 'Our attempt at the first software assignment.',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
