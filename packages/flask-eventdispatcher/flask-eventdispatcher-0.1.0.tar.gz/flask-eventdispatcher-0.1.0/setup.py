# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

modules = \
['flask_eventdispatcher']
install_requires = \
['blinker>=1.4,<2.0', 'flask>=1.1,<2.0']

setup_kwargs = {
    'name': 'flask-eventdispatcher',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Anton Ruhlov',
    'author_email': 'antonruhlov@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
