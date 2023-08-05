# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['airflow_docker_compose']

package_data = \
{'': ['*']}

install_requires = \
['click', 'docker', 'docker-compose', 'python-dotenv', 'toml']

entry_points = \
{'console_scripts': ['airflow-docker-compose = '
                     'airflow_docker_compose.__main__:run']}

setup_kwargs = {
    'name': 'airflow-docker-compose',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Dan Cardin',
    'author_email': 'ddcardin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/airflowdocker/airflow-docker-compose',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5.0',
}


setup(**setup_kwargs)
