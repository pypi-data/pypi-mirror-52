# flake8-import-order-ruler501

A [flake8-import-order](https://github.com/PyCQA/flake8-import-order) ordering definition, defining ruler501's preferred import order style. Originally based on [flake8-import-order-grok](https://github.com/groklearning/flake8-import-order-grok)

The import order enforced by this style is:
1. `__future__`
2. builtins
3. third-party, grouped separately by package
4. Application packages by package
5. Relative imports

All groups of imports require a line break between them, except packages within your application.

All imports must be alphabetical horizontally and vertically.
`from` import groups are on separate lines sorted by constants first, followed by classes, followed by functions (i.e. CAPITAL_CASE, CamelCase, underscore_case).

The names of the application packages can be configured via the `application-import-names` setting in `flake8`.

For example, if `application-import-names` is set to `my_project`, this import ordering enforces the following ordering:

```python
# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals  # 1. `__future__`

import io  # 2. Builtins.
import logging
import os
import tarfile

from django.conf import settings  # 3.1 django
from django.utils.http import urlencode

from dns.exception import DNSException, Timeout  # 3.2
from dns.resolver import NXDOMAIN
from dns.resolver import NoAnswer, Resolver

import requests # 3.3 

import ujson #3.4

from my_project.views import MainView  # 4. Application packages.
from my_project.core.enums import Enum
from my_project.utils.download import DOWNLOAD_TIMEOUT
from my_project.utils.download import InvalidURLException
from my_project.utils.download import download_content_url

from .models import Article
```

## Usage

Install the `flake8-import-order-ruler501` package using `pip`, then tell `flake8` to use this import order style using the `--import-order-style=ruler501` command-line option, or by setting it in `setup.cfg`.
The names of your application package(s) can be set by the `application-import-names` setting:

```
[flake8]
import-order-style = ruler501
application-import-names = my_package1, my_package2
```
