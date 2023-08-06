# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['opset']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.1,<0.5.0',
 'munch>=2.3,<3.0',
 'python-logstash>=0.4.6,<0.5.0',
 'pytz>=2018.9,<2019.0',
 'pyyaml>=3.13,<6',
 'structlog>=19.1,<20.0']

setup_kwargs = {
    'name': 'opset',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Alexandre Jutras',
    'author_email': 'alexandre.jutras@elementai.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
