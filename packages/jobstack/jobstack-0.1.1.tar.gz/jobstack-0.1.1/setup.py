# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['jobstack', 'jobstack.resources']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0', 'jinja2>=2.10,<3.0', 'pendulum>=2.0,<3.0']

entry_points = \
{'console_scripts': ['jobstack = jobstack:app.main']}

setup_kwargs = {
    'name': 'jobstack',
    'version': '0.1.1',
    'description': 'Commandline utility for organizing and scheduling project tasks across a team.',
    'long_description': '#### JobStack\n\nCommandline utility for organizing and scheduling project tasks.\n\n\n',
    'author': 'Mark Gemmill',
    'author_email': 'mark@markgemmill.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
