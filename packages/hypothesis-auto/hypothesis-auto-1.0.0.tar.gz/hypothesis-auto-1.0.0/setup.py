# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hypothesis_auto']

package_data = \
{'': ['*']}

install_requires = \
['hypothesis>=4.36,<5.0', 'pydantic>=0.32.2,<0.33.0']

extras_require = \
{'pytest': ['pytest>=4.0.0,<5.0.0']}

setup_kwargs = {
    'name': 'hypothesis-auto',
    'version': '1.0.0',
    'description': 'Extends Hypothesis to add fully automatic testing of type annotated functions',
    'long_description': "[![hypothesis-auto - Fully Automatic Tests for Type Annotated Functions Using Hypothesis.](https://raw.github.com/timothycrosley/hypothesis-auto/master/art/logo_large.png)](https://timothycrosley.github.io/hypothesis-auto/)\n_________________\n\n[![PyPI version](https://badge.fury.io/py/hypothesis-auto.svg)](http://badge.fury.io/py/hypothesis-auto)\n[![Build Status](https://travis-ci.org/timothycrosley/hypothesis-auto.svg?branch=master)](https://travis-ci.org/timothycrosley/hypothesis-auto)\n[![codecov](https://codecov.io/gh/timothycrosley/hypothesis-auto/branch/master/graph/badge.svg)](https://codecov.io/gh/timothycrosley/hypothesis-auto)\n[![Join the chat at https://gitter.im/timothycrosley/hypothesis-auto](https://badges.gitter.im/timothycrosley/hypothesis-auto.svg)](https://gitter.im/timothycrosley/hypothesis-auto?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/hypothesis-auto/)\n[![Downloads](https://pepy.tech/badge/hypothesis-auto)](https://pepy.tech/project/hypothesis-auto)\n_________________\n\n[Read Latest Documentation](https://timothycrosley.github.io/hypothesis-auto/) - [Browse GitHub Code Repository](https://github.com/timothycrosley/hypothesis-auto/)\n_________________\n\nAn extension for the hypothesis project that enables fully automatic tests for type annotated functions:\n\n```python3\nfrom hypothesis_auto import auto_test\n\n\ndef add(number_1: int, number_2: int = 1) -> int:\n    return number_1 + number_2\n\n\nauto_test(add)  # 50 property based scenerios are generated and ran against add\nauto_test(add, _auto_runs=1_000)  # Let's make that 1,000\n```\n\n\n```python3\nfrom hypothesis_auto import auto_test\n\n\ndef divide(number_1: int, number_2: int) -> int:\n    return number_1 / number_2\n\nauto_test(divide)\n\n-> 1012                     raise the_error_hypothesis_found\n   1013\n   1014         for attrib in dir(test):\n\n<ipython-input-2-65a3aa66e9f9> in divide(number_1, number_2)\n      1 def divide(number_1: int, number_2: int) -> int:\n----> 2     return number_1 / number_2\n      3\n\n0/0\n\nZeroDivisionError: division by zero\n\n\nauto_test(divide, _auto_allow_exceptions=(ZeroDivisionError, ))\n```\n\nFor the full set of parameters you can pass into auto_test see its [API reference documentation](https://timothycrosley.github.io/hypothesis-auto/reference/hypothesis_auto/tester/).\n\n## Why Create hypothesis-auto?\n\nI wanted a no/low resistance way to start incorporating property based tests across my projects. Such a solution, that also encouraged the use of type hints, was a win/win for me.\n\nI hope you too find `hypothesis-auto` useful!\n\n~Timothy Crosley\n",
    'author': 'Timothy Crosley',
    'author_email': 'timothy.crosley@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
