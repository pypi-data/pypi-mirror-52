# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['docker_image_size_limit']

package_data = \
{'': ['*']}

install_requires = \
['docker>=3.7,<5.0', 'humanfriendly>=4.18,<5.0']

entry_points = \
{'console_scripts': ['disl = docker_image_size_limit:main']}

setup_kwargs = {
    'name': 'docker-image-size-limit',
    'version': '0.2.0',
    'description': '',
    'long_description': '# docker-image-size-limit\n\n[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services) [![Build Status](https://travis-ci.org/wemake-services/docker-image-size-limit.svg?branch=master)](https://travis-ci.org/wemake-services/docker-image-size-limit) [![Coverage](https://coveralls.io/repos/github/wemake-services/docker-image-size-limit/badge.svg?branch=master)](https://coveralls.io/github/wemake-services/docker-image-size-limit?branch=master) [![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/docker-image-size-limit)\n\nLimit your `docker` image size with a simple CLI command.\nPerfect to be used inside your CI process.\n\nRead the [announcing post](https://sobolevn.me/2019/03/announcing-docker-image-size-limit).\n\n\n## Installation\n\n```bash\npip install docker-image-size-limit\n```\n\n\n## Usage\n\nWe support just a single command:\n\n```bash\n$ disl your-image-name:label 300MiB\nyour-image-name:label exceeds 300MiB limit by 114.4 MiB\n```\n\n\n## Options\n\nYou can specify your image as:\n\n- Image name: `python`\n- Image name with tag: `python:3.6.6-alpine`\n\nYou can specify your size as:\n\n- Raw number of bytes: `1024`\n- Human-readable megabytes: `30 MB` or `30 MiB`\n- Human-readable gigabytes: `1 GB` or `1 GiB`\n- Any other size supported by [`humanfriendly`](https://humanfriendly.readthedocs.io/en/latest/api.html#humanfriendly.parse_size)\n\n\n## Programmatic usage\n\nYou can also import and use this library as `python` code:\n\n```python\nfrom docker import from_env\nfrom docker_image_size_limit import check_image_size\n\noversize = check_image_size(client, \'image-name:latest\', \'1 GiB\')\nassert oversize < 0, \'Too big image!\'  # negative oversize - is a good thing!\n```\n\nWe also ship [PEP-561](https://www.python.org/dev/peps/pep-0561/)\ncompatible type annotations with this library.\n\n\n## Should I use it?\n\nYou can use this script instead:\n\n```bash\nLIMIT=1024\nIMAGE=\'your-image-name:latest\'\n\nSIZE="$(docker image inspect "$IMAGE" --format=\'{{.Size}}\')"\ntest "$SIZE" -gt "$LIMIT" && echo \'Limit exceeded\'; false\n```\n\nBut I prefer to reuse tools over\ncustom `bash` scripts here and there.\n\n\n## License\n\nMIT.\n',
    'author': 'Nikita Sobolev',
    'author_email': 'mail@sobolevn.me',
    'url': 'https://github.com/wemake-services/docker-image-size-limit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
