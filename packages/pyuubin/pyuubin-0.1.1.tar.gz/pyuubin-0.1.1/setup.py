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
    'version': '0.1.1',
    'description': 'Mailing services with HTTP Api',
    'long_description': "# 💨💨💨 Pyuubin – Mailing System 💨💨💨\n\n[![Build Status](https://travis-ci.org/MichalMazurek/pyuubin.svg?branch=master)](https://travis-ci.org/MichalMazurek/pyuubin)\n\nAsynchronous mailing system over HTTP API.\n\n郵便 (Yūbin) - Postal Service\n\nぴゅー (Pyu-) – SFX for a sudden burst of speed, like running away from something\n\n## Installation\n\n```bash\npip install pyuubin\n```\n\n## Installation from source\n\n```bash\npip install .\n```\n\n## Running the service\n\nYou need to run the API and Worker for the system to work.\n\n### The API\n\nUse hypercorn or uvicorn to run it\n\n```bash\nhypercorn pyuubin.api.app:app --access-log - --error-log -\n```\n\n### The Worker\n\n```bash\n$ python -m pyuubin.worker --help\nUsage: worker.py [OPTIONS]\n\n  Run the worker.\n\nOptions:\n  -n, --name TEXT                 Name of the service\n  -w, --workers INTEGER           Number of workers\n  -d, --debug                     Enable debug mode.\n  -e, --print-environment-variables\n                                  print environment variables to be put in\n                                  .env file for configuration\n  --help                          Show this message and exit.\n```\n\n## Configuration\n\nYou can configure Pyuubin by using environmental variables. List of variables is available on running\n\n```bash\n$ python -m pyuubin -e\nPYUUBIN_REDIS_PREFIX=pyuubin:\nPYUUBIN_REDIS_MAIL_QUEUE=pyuubin::mail_queue\nPYUUBIN_REDIS_URL=redis://localhost:6379\nPYUUBIN_SMTP_HOST=smtp.gmail.com\nPYUUBIN_SMTP_PORT=465\nPYUUBIN_SMTP_USER=email@gmail.com\nPYUUBIN_SMTP_PASSWORD=SecretStr('**********')\nPYUUBIN_SMTP_TLS=True\nPYUUBIN_MAIL_FROM=email@gmail.com\nPYUUBIN_MAIL_RETURN=returns@exampple.tld\nPYUUBIN_MAIL_CONNECTOR=pyuubin.connectors.smtp\nPYUUBIN_AUTH_HTPASSWD_FILE=\n```\n\n> Note that the password is a `SecretStr` type from pydantic, so in your `.env.` file please just write your password without `SecretStr()`, so actually what you want is: `PYUUBIN_SMTP_PASSWORD=secret`\n\nPyuubin supports `.env` files. You can create one quite easily by running above command and directing the output to a `.env` file.\n\n```bash\n$ python -m pyuubin -e > .env\n$\n```\n\nThen edit this file, put the values required and run the app.\n\n## Authentication - Password File\n\nGenerating passwords with htpasswd:\n\n```bash\nhtpasswd -Bc test_htpasswd app1\n```\n\n> Note: Only blowfish encrypted hashes are supported\n\n## API Specification\n\nYou can find API docs here: [redoc pages](https://pyuubin.io/docs/index.html)\n\n## TODO\n\n- Documentation\n- Client library\n- Handling of rejected/failed mails\n- Bounces management\n- Rate limitting for source / global\n",
    'author': 'Michal Mazurek',
    'author_email': 'mazurek.michal@gmail.com',
    'url': 'https://pyuubin.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
