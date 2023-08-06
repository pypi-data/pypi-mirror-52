# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cloudgarden']

package_data = \
{'': ['*'],
 'cloudgarden': ['aws/*',
                 'aws/resources/*',
                 'diagram/*',
                 'infrastructure/*',
                 'marshalling/*',
                 'marshalling/diagram/*']}

install_requires = \
['boto3>=1.9.232,<2.0.0', 'marshmallow>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'cloudgarden',
    'version': '0.1.3',
    'description': 'Cloudgarden basic library',
    'long_description': None,
    'author': 'Elendir',
    'author_email': 'mich.spicka.ja+pypi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
