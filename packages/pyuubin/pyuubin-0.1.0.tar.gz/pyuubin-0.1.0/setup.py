# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyuubin', 'pyuubin.api', 'pyuubin.connectors']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.2,<2.0',
 'aiosmtplib>=1.0,<2.0',
 'bcrypt>=3.1,<4.0',
 'click>=7.0,<8.0',
 'coloredlogs>=10.0,<11.0',
 'email-validator>=1.0,<2.0',
 'envparse>=0.2.0,<0.3.0',
 'fastapi>=0.38.1,<0.39.0',
 'html2text>=2018.1,<2019.0',
 'hypercorn>=0.6.0,<0.7.0',
 'jinja2>=2.10,<3.0',
 'msgpack>=0.6.1,<0.7.0',
 'pydantic>=0.32.2,<0.33.0',
 'python-dotenv>=0.10.3,<0.11.0',
 'tblib>=1.3,<2.0',
 'trio>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'pyuubin',
    'version': '0.1.0',
    'description': 'Mailing services with HTTP Api',
    'long_description': None,
    'author': 'Michal Mazurek',
    'author_email': 'michal@mazurek-inc.co.uk',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
