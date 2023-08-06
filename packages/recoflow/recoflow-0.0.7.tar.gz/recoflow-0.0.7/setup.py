# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['recoflow']

package_data = \
{'': ['*']}

install_requires = \
['altair>=3.2,<4.0',
 'keras>=2.3,<3.0',
 'matplotlib>=3.1,<4.0',
 'numpy>=1.17,<2.0',
 'pandas>=0.25.1,<0.26.0',
 'requests>=2.22,<3.0',
 'scikit-learn>=0.21.3,<0.22.0']

setup_kwargs = {
    'name': 'recoflow',
    'version': '0.0.7',
    'description': 'Deep Recommender System for Humans',
    'long_description': '# recoflow\nDeep Recommender System for Humans\n',
    'author': 'Amit Kapoor',
    'author_email': 'amitkaps@gmail.com',
    'url': 'https://github.com/amitkaps/recoflow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
