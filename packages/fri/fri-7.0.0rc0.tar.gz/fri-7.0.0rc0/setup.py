# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fri', 'fri.model', 'fri.toydata']

package_data = \
{'': ['*'], 'fri': ['tests/*']}

install_requires = \
['cvxpy==1.0.24',
 'ecos>=2.0.5,<3.0.0',
 'joblib>=0.13.2,<0.14.0',
 'matplotlib>=3.1,<4.0',
 'numpy>=1.17,<2.0',
 'scikit-learn>=0.21.1,<0.22.0',
 'scipy>=1.0,<2.0']

setup_kwargs = {
    'name': 'fri',
    'version': '7.0.0rc0',
    'description': 'Implementation of Feature Relevance Bounds method to perform Feature Selection and further analysis.',
    'long_description': None,
    'author': 'Lukas Pfannschmidt',
    'author_email': 'lukas@lpfann.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://fri.lpfann.me',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
