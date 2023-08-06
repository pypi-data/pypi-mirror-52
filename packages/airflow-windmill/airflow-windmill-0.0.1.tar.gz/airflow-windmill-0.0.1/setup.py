# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['windmill',
 'windmill.cli',
 'windmill.config',
 'windmill.http',
 'windmill.http.api',
 'windmill.models',
 'windmill.models.dags',
 'windmill.models.operators',
 'windmill.models.schemas',
 'windmill.tasks',
 'windmill.utils']

package_data = \
{'': ['*'],
 'windmill.http': ['app/*',
                   'app/dist/*',
                   'app/public/*',
                   'app/src/*',
                   'app/src/components/*',
                   'app/src/components/Airflow/*',
                   'app/src/components/Navbar/*',
                   'app/src/components/Page/*',
                   'app/src/components/Sidebar/*',
                   'app/src/misc/*']}

install_requires = \
['decli>=0.5.1,<0.6.0',
 'docstring-parser>=0.3.0,<0.4.0',
 'flask-cors>=3.0.8,<4.0.0',
 'marshmallow>=3.0,<4.0',
 'pyyaml>=5.1.2,<6.0.0']

extras_require = \
{'airflow': ['apache-airflow==1.10.4']}

entry_points = \
{'console_scripts': ['windmill = windmill:cli.cli.Cli.run_cli',
                     'windmill-dev = windmill:cli.cli.DevCli.run_cli']}

setup_kwargs = {
    'name': 'airflow-windmill',
    'version': '0.0.1',
    'description': "Drag'N'Drop Web Frontend for Building and Managing Airflow DAGs",
    'long_description': "# Windmill\n\n[![Build Status](https://travis-ci.org/mayansalama/windmill.svg?branch=master)](https://travis-ci.org/mayansalama/windmill)\n\nDrag'n'drop web app to manage and create Airflow DAGs. The goal is to\nhave a Web UI that can generate YML Dag Definitions, integrating with\ncustom operators and potentially existing DAGs. YML DAGs can then be\nsynced to a remote repo\n\n- Front end is built using React on Typescript\n- Back end is built using Flask on Python 3.6+\n\n## Getting Started\n\n1. Install with `pip install airflow-windmill`\n   1. Airflow is expected to be installed on the system\n   2. Otherwise it can be packaged with windmill using `pip install airflow-windmill[airflow]`\n2. Run `windmill init` to create a local Windmill project\n3. `cd windmill-project`\n4. Run `windmill run` from this folder to run the app locally\n\n## MVP Required Features\n\n### Front-End Features\n\n- [x] Dynamic Operators\n- [x] Menu Dropdowns\n- [x] Load Operators from App\n- [x] Format operator display into classes\n- [x] Search functionality for operators\n- [x] Basic operator level properties\n- [x] Implement DAG level properties\n- [x] New DAG Functionality\n- [x] Parameter Tooltips\n- [x] Render arbitrary viewport windows for New/Save/Load etc\n- [x] Overwrite/Save prompt on New\n- [x] DAG renaming and save functionality\n- [x] Open dag from menu\n- [ ] Switch nav menu to icons\n- [ ] Make input/output nodes more clear\n- [ ] Make save/load more efficient by removing non-essential values\n- [ ] Check if file already exists on rename\n- [ ] Prompt save if there are nodes on open\n- [ ] Fix loss of state on refresh bug\n- [ ] Put File details in File Browser\n- [ ] Make Flask Backend URI configurable\n- [ ] Add a last saved time to NavBar\n\n### Back-End Features\n\n- [x] Generate Operator Lists\n- [x] CLI to start Web and Front End\n- [x] Generate DAG Spec\n- [x] CLI to create new windmill project\n- [x] CLI to start windmill from a windmill project\n- [x] Implement windmill-dev start\n- [x] Save/Load Windmill Files functionality\n- [x] Get default values\n- [x] Pull parameters from parent classes\n- [ ] Move airflow dependency as extra\n- [ ] ? Dedupe multi import operators - nothing preventing this but underlying issue is fixed\n- [ ] Convert WML into Python DAG\n- [ ] Get WML owner and last-modified details during wml list\n- [ ] Allow custom operators\n- [ ] Add defaults to CLI --help commands\n- [ ] Strategy for Python Opjects (e.g. callables) - maybe import statement?\n- [ ] Backport existing Python DAGs to WMLs\n- [ ] Allow YML updates to propogate to WMLs\n\n### Other features\n\n- [ ] Validate on backend or front end or both?\n- [ ] Doco\n\n## Dev User Guide\n\nTo run as a dev:\n\n1. Clone from git\n2. Run `poetry install`\n3. Run `windmill-dev start-backend`\n4. Run `windmill-dev start-frontend`\n\n## Future Usage Patterns\n\n- Auto-sync for windmill project to git\n\n## Deployment\n\n```bash\ncd scripts\nsh build.sh {{PYPI_USER}} {{PYPI_PASS}}\n```\n",
    'author': 'mayansalama',
    'author_email': 'micsalama@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
