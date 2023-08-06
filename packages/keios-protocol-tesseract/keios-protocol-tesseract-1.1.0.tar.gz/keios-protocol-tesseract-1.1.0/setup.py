# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['keios_protocol_tesseract']

package_data = \
{'': ['*'], 'keios_protocol_tesseract': ['flatbuffers/*']}

install_requires = \
['flatbuffers==1.11']

setup_kwargs = {
    'name': 'keios-protocol-tesseract',
    'version': '1.1.0',
    'description': '',
    'long_description': None,
    'author': 'Leftshift One',
    'author_email': 'contact@leftshift.one',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
