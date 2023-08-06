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
    'version': '1.0.1',
    'description': 'Extends Hypothesis to add fully automatic testing of type annotated functions',
    'long_description': "[![hypothesis-auto - Fully Automatic Tests for Type Annotated Functions Using Hypothesis.](https://raw.github.com/timothycrosley/hypothesis-auto/master/art/logo_large.png)](https://timothycrosley.github.io/hypothesis-auto/)\n_________________\n\n[![PyPI version](https://badge.fury.io/py/hypothesis-auto.svg)](http://badge.fury.io/py/hypothesis-auto)\n[![Build Status](https://travis-ci.org/timothycrosley/hypothesis-auto.svg?branch=master)](https://travis-ci.org/timothycrosley/hypothesis-auto)\n[![codecov](https://codecov.io/gh/timothycrosley/hypothesis-auto/branch/master/graph/badge.svg)](https://codecov.io/gh/timothycrosley/hypothesis-auto)\n[![Join the chat at https://gitter.im/timothycrosley/hypothesis-auto](https://badges.gitter.im/timothycrosley/hypothesis-auto.svg)](https://gitter.im/timothycrosley/hypothesis-auto?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/hypothesis-auto/)\n[![Downloads](https://pepy.tech/badge/hypothesis-auto)](https://pepy.tech/project/hypothesis-auto)\n_________________\n\n[Read Latest Documentation](https://timothycrosley.github.io/hypothesis-auto/) - [Browse GitHub Code Repository](https://github.com/timothycrosley/hypothesis-auto/)\n_________________\n\n**hypothesis-auto** is an extension for the [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) project that enables fully automatic tests for type annotated functions.\n\n[![Hypothesis Pytest Auto Example](https://raw.github.com/timothycrosley/hypothesis-auto/master/art/demo.gif)](https://github.com/timothycrosley/hypothesis-auto/blob/master/art/demo.gif)\n\nKey Features:\n\n* **Type Annotation Powered**: Utilize your function's existing type annotations to build dozens of test cases automatically.\n* **Low Barrier**: Start utilizing property-based testing in the lowest barrier way possible. Just run `auto_test(FUNCTION)` to run dozens of test.\n* **py.test Compatible**: Built-n compatibility with the popular [py.test](https://docs.pytest.org/en/latest/) testing framework. This means that you can turn your automatically generated tests into individual py.test test cases with one line.\n* **Scales Up**: As you find your self needing to customize your auto_test cases, you can easily utilize all the features of [Hypothesis](https://hypothesis.readthedocs.io/en/latest/), including custom strategies per a parameter.\n\n## Installation:\n\nTo get started - install `hypothesis-auto` into your projects virtual environment:\n\n`pip3 install hypothesis-auto`\n\nOR\n\n`poetry add hypothesis-auto`\n\nOR\n\n`pipenv install hypothesis-auto`\n\n## Usage Examples:\n\n### Framework independent usage\n\nBasic `auto_test` usage:\n\n```python31\nfrom hypothesis_auto import auto_test\n\n\ndef add(number_1: int, number_2: int = 1) -> int:\n    return number_1 + number_2\n\n\nauto_test(add)  # 50 property based scenerios are generated and ran against add\nauto_test(add, _auto_runs=1_000)  # Let's make that 1,000\n```\n\nAdding an allowed exception:\n\n```python3\nfrom hypothesis_auto import auto_test\n\n\ndef divide(number_1: int, number_2: int) -> int:\n    return number_1 / number_2\n\nauto_test(divide)\n\n-> 1012                     raise the_error_hypothesis_found\n   1013\n   1014         for attrib in dir(test):\n\n<ipython-input-2-65a3aa66e9f9> in divide(number_1, number_2)\n      1 def divide(number_1: int, number_2: int) -> int:\n----> 2     return number_1 / number_2\n      3\n\n0/0\n\nZeroDivisionError: division by zero\n\n\nauto_test(divide, _auto_allow_exceptions=(ZeroDivisionError, ))\n```\n\nFor the full set of parameters, you can pass into auto_test see its [API reference documentation](https://timothycrosley.github.io/hypothesis-auto/reference/hypothesis_auto/tester/).\n\n### py.test usage\n\nUsing `auto_pytest_magic` to auto-generate dozens of py.test test cases:\n\n```python3\nfrom hypothesis_auto import auto_pytest_magic\n\n\ndef add(number_1: int, number_2: int = 1) -> int:\n    return number_1 + number_2\n\n\nauto_pytest_magic(add)\n```\n\nUsing `auto_pytest` to run dozens of test case within a temporary directory:\n\n```\nfrom hypothesis_auto import auto_pytest\n\n\ndef add(number_1: int, number_2: int = 1) -> int:\n    return number_1 + number_2\n\n\n@auto_pytest()\ndef test_add(test_case, tmpdir):\n    tmpdir.mkdir().chdir()\n    test_case()\n```\n\nFor the full reference of the py.test integration API see the [API reference documentation](https://timothycrosley.github.io/hyp othesis-auto/reference/hypothesis_auto/pytest/).\n\n## Why Create hypothesis-auto?\n\nI wanted a no/low resistance way to start incorporating property-based tests across my projects. Such a solution that also encouraged the use of type hints was a win/win for me.\n\nI hope you too find `hypothesis-auto` useful!\n\n~Timothy Crosley\n",
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
