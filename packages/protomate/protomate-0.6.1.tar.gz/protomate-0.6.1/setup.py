# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['protomate']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub==1.43.8',
 'art==4.0',
 'colorama==0.4.1',
 'keyring==17.1.1',
 'loguru==0.3.2',
 'prompt_toolkit==2.0.9',
 'questionary==1.3.0',
 'sty==1.0.0b12',
 'termcolor==1.1.0']

entry_points = \
{'console_scripts': ['protomate = protomate.script:main']}

setup_kwargs = {
    'name': 'protomate',
    'version': '0.6.1',
    'description': 'Python built CLI tool for automated github project initialization.',
    'long_description': '<div align="center">  \n  \n# Protomate\n\n\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/rednafi/protomate/blob/master/LICENSE) ![stability-experimental](https://img.shields.io/badge/stability-experimental-orange.svg) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)\n\n<img src="https://github.com/rednafi/protomate/blob/master/demo/demo.svg" width="900" height="600">\n\n</div>\n\nThis will perform the following tasks:\n\n- Create a new project folder in your **current** folder\n- Ask for your username and password (and also if you\'d like to save your password)\n- Initialize a git repository\n- Create a remote repository\n- Add remote to the local repository\n- Add a `readme.md` file\n- Add a `.gitignore` file specific for your language of choice\n- Perform initial stage, commit, push\n- Try to open the project folder in vscode\n\n## Installation\n\nInstall `protomate` via:\n\n```\n$ pip3 install protomate==0.6.1\n```\n\n## Run the App\n\nTo create a new project in your designated project folder, first `cd` to your desired location:\n\n```\n$ cd project-location\n```\n\nTo initialize the CLI, type:\n\n```\n$ protomate\n```\n\nThis should:\n\n- Prompt you to put your\n\n  - Github credentials\n  - Repository name\n  - Repository type (public/private)\n  - Language of `.gitignore` (python, javascript etc). See a list of all the supported [languages](https://github.com/rednafi/protomate/blob/master/protomate/languages.py).\n\n- Create a new local and remote git repository\n\n- Connect them and open vs code for you to start coding immediately\n\n## Contributor\n* Redowan Delowar (Author & primary maintainer) [@rednafi](https://github.com/rednafi)\n* Manash Kumar Mandal [@manashmndl](https://github.com/manashmndl)\n',
    'author': 'Redowan Delowar',
    'author_email': None,
    'url': 'https://github.com/rednafi/protomate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
