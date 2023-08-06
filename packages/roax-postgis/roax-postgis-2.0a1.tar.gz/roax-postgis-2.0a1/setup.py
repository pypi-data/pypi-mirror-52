# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['roax']

package_data = \
{'': ['*']}

install_requires = \
['roax-geo>=2.0a1,<3.0', 'roax-postgresql>=2.0a1,<3.0']

setup_kwargs = {
    'name': 'roax-postgis',
    'version': '2.0a1',
    'description': 'PostGIS extension for Roax.',
    'long_description': '# Roax-PostGIS\n\n[![PyPI](https://badge.fury.io/py/roax-postgis.svg)](https://badge.fury.io/py/roax-postgis)\n[![License](https://img.shields.io/github/license/roax/roax-postgis.svg)](https://github.com/roax/roax-postgis/blob/master/LICENSE)\n[![GitHub](https://img.shields.io/badge/github-master-blue.svg)](https://github.com/roax/roax-postgis/)\n[![Travis CI](https://travis-ci.org/roax/roax-postgis.svg?branch=master)](https://travis-ci.org/roax/roax-postgis)\n[![Codecov](https://codecov.io/gh/roax/roax-postgis/branch/master/graph/badge.svg)](https://codecov.io/gh/roax/roax-postgis)\n[![Black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)\n\nRoax-PostGIS: PostGIS extension for Roax.\n\n## Develop\n\n```\npoetry install\npoetry run pre-commit install\n```\n\n## Test\n\n```\npoetry run pytest\n```\n',
    'author': 'Paul Bryan',
    'author_email': 'pbryan@anode.ca',
    'url': 'https://github.com/roax/roax-postgis/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
