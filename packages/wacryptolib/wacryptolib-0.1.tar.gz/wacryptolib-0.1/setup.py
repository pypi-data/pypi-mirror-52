# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['wacryptolib']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'pycryptodome>=3.9,<4.0',
 'pymongo>=3.9,<4.0',
 'schema>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'wacryptolib',
    'version': '0.1',
    'description': 'Witness Angel Cryptolib',
    'long_description': 'Witness Angel Cryptolib\n#############################\n\nThis lib gathers useful utilities to generate keys, and encrypt/descrypt/sign data, for the\nWitness Angel system.\n\n\nPrerequisites\n==================\n\nYou will need:\n\n- `python3.7` (see `pyproject.toml` for full version)\n\n\nDevelopment\n===================\n\nWhen developing locally, we use:\n\n- [`poetry`](https://github.com/sdispater/poetry) (**required**)\n\nUse "pip install poetry" to install poetry (or follow its official docs to inside it system-wide).\n\nUse "poetry install" to install python dependencies.\n\nUse "pytest" to launch unit-tests; its default arguments are in setup.cfg\n\nUse "bash ci.sh" to launch sources checkup, before committing or pushing your changes.\n\nUse Black formatter (or integrate it as an onsave-hook in your IDE) to format python sources.\n',
    'author': 'Pascal Chambon',
    'author_email': None,
    'url': 'https://github.com/WitnessAngel/witness-angel-cryptolib',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
