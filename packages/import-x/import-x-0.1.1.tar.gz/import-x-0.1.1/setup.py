# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['import_x', 'import_x.loaders']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'import-x',
    'version': '0.1.1',
    'description': 'Import non-python files',
    'long_description': '<p align="center">\n  <img src="https://deepsource.io/images/logo-wordmark-dark.svg" />\n</p>\n\n<p align="center">\n  <a href="https://deepsource.io/docs">Documentation</a> |\n  <a href="https://deepsource.io/signup">Get Started</a> |\n  <a href="https://gitter.im/deepsourcelabs/lobby?utm_source=share-link&utm_medium=link&utm_campaign=share-link">Developer Chat</a>\n</p>\n\n<p align="center">\n  DeepSource helps you ship good quality code.\n</p>\n\n</p>\n\n---\n\n# import-x\n\nAn ext-tensible loader to import anything like it is a python module.\n\nSupports Python **3.6+**.\n\n## Installation\n\n```\npip install import-x\n```\n\n## Usage\n\nExample json file in your path ``foo.json``:\n\n```json\n    {\n        "why": "not",\n    }\n```\n\n```python\n   # Extend the ExtensionLoader and implement \'handle_module\' method\n   # where you will get a module object and the path to that module.\n\n   >>> from import_x import ExtensionLoader\n\n   >>> class JsonLoader(ExtensionLoader):\n        extension = \'.json\'\n\n        auto_enable = False\n\n        @staticmethod\n        def handle_module(module, path):\n            """\n            Load the json file and set as `data` attribute of the module.\n            """\n            json_file = Path(path)\n            content = json_file.read_text()\n            try:\n                data = json.loads(content)\n            except (json.JSONDecodeError, ValueError):\n                data = {}\n            module.data = data\n\n    >>> json_imports = JsonLoader()\n    >>> with json_imports:\n            import foo\n    >>> foo.data\n    >>> {"why": "not"}\n```\n\nIf you want to enable imports automatically without the context_manager then just\ndo ``auto_enable = True`` in your loader.\n\nThis Example ``JsonLoader`` can be used directly by importing\n\n```python\n    from import_x.loaders.json_loader import JsonLoader\n```\n\nand you are ready to import all the json files.\n',
    'author': 'Mohit Solanki',
    'author_email': 'mohit@deepsource.io',
    'url': 'https://github.com/deepsourcelabs/import-x',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
