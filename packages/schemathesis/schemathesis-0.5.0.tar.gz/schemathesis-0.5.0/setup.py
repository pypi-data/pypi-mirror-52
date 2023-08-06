# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['schemathesis', 'schemathesis.extra']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.1,<20.0',
 'hypothesis>=4.32,<5.0',
 'hypothesis_jsonschema>=0.9.7,<0.10.0',
 'jsonschema>=3.0.0,<4.0.0',
 'pytest>4.6.4',
 'pyyaml>=5.1,<6.0']

entry_points = \
{'pytest11': ['schemathesis = schemathesis.extra.pytest_plugin']}

setup_kwargs = {
    'name': 'schemathesis',
    'version': '0.5.0',
    'description': 'Hypothesis strategies for Open API / Swagger schemas',
    'long_description': 'Schemathesis\n============\n\n|Build| |Version| |Python versions| |License|\n\nSchemathesis is a tool for testing your web applications built with Open API / Swagger specifications.\n\nIt reads the application schema and generates test cases which will ensure that your application is compliant with its schema.\n\nThe application under test could be written in any language, the only thing you need is a valid API schema in a supported format.\n\n**Supported specification versions**:\n\n- Swagger 2.0\n- Open API 3.0.x\n\nMore API specifications will be added in the future.\n\nBuilt with:\n\n- `hypothesis`_\n\n- `hypothesis_jsonschema`_\n\n- `pytest`_\n\nInstallation\n------------\n\nTo install Schemathesis via ``pip`` run the following command:\n\n.. code:: bash\n\n    pip install schemathesis\n\nOptionally you could install ``requests`` for convenient HTTP calls.\n\nUsage\n-----\n\nTo examine your application with Schemathesis you need to:\n\n- Setup & run your application, so it is accessible via the network;\n- Write a couple of tests in Python;\n- Run the tests via ``pytest``.\n\nSuppose you have your application running on ``http://0.0.0.0:8080`` and its\nschema is available at ``http://0.0.0.0:8080/swagger.json``.\n\nA basic test, that will verify that any data, that fit into the schema will not cause any internal server error could\nlook like this:\n\n.. code:: python\n\n    # test_api.py\n    import pytest\n    import requests\n    import schemathesis\n\n    BASE_URL = "http://0.0.0.0:8080"\n    schema = schemathesis.from_uri(f"{BASE_URL}/swagger.json")\n\n    @schema.parametrize()\n    def test_no_server_errors(case):\n        response = requests.request(\n            case.method,\n            f"{BASE_URL}{case.formatted_path}",\n            headers=case.headers,\n            params=case.query,\n            json=case.body\n        )\n        assert response.status_code < 500\n\n\nIt consists of four main parts:\n\n1. Schema preparation; ``schemathesis`` package provides multiple ways to initialize the schema - ``from_path``, ``from_dict``, ``from_uri``, ``from_file``.\n\n2. Test parametrization; ``@schema.parametrize()`` generates separate tests for all endpoint/method combination available in the schema.\n\n3. A network call to the running application; ``requests`` will do the job, for example.\n\n4. Verifying a property you\'d like to test; In the example, we verify that any app response will not indicate a server-side error (HTTP codes 5xx).\n\nRun the tests:\n\n.. code:: bash\n\n    pytest test_api.py\n\n**Other properties that could be tested**:\n\n- Any call will be processed in <50 ms - you can verify the app performance;\n- Any unauthorized access will end with 401 HTTP response code;\n\nEach test function should have the ``case`` fixture, that represents a single test case.\n\nImportant ``Case`` attributes:\n\n- ``method`` - HTTP method\n- ``formatted_path`` - full endpoint path\n- ``headers`` - HTTP headers\n- ``query`` - query parameters\n- ``body`` - request body\n\nFor each test, Schemathesis will generate a bunch of random inputs acceptable by the schema.\nThis data could be used to verify that your application works in the way as described in the schema or that schema describes expected behavior.\n\nBy default, there will be 100 test cases per endpoint/method combination.\nTo limit the number of examples you could use ``hypothesis.settings`` decorator on your test functions:\n\n.. code:: python\n\n    from hypothesis import settings\n\n    @settings(max_examples=5)\n    def test_something(client, case):\n        ...\n\nExplicit examples\n~~~~~~~~~~~~~~~~~\n\nIf the schema contains parameters examples, then they will be additionally included in the generated cases.\n\n.. code:: yaml\n\n    paths:\n      get:\n        parameters:\n        - in: body\n          name: body\n          required: true\n          schema: \'#/definitions/Pet\'\n\n    definitions:\n      Pet:\n        additionalProperties: false\n        example:\n          name: Doggo\n        properties:\n          name:\n            type: string\n        required:\n        - name\n        type: object\n\n\nWith this Swagger schema example, there will be a case with body ``{"name": "Doggo"}``.  Examples handled with\n``example`` decorator from Hypothesis, more info about its behavior is `here`_.\n\nNOTE. Schemathesis supports only examples in ``parameters`` at the moment, examples of individual properties are not supported.\n\nDocumentation\n-------------\n\nFor the full documentation, please see https://schemathesis.readthedocs.io/en/latest/ (WIP)\n\nOr you can look at the ``docs/`` directory in the repository.\n\nPython support\n--------------\n\nSchemathesis supports Python 3.6, 3.7 and 3.8.\n\nLicense\n-------\n\nThe code in this project is licensed under `MIT license`_.\nBy contributing to ``schemathesis``, you agree that your contributions\nwill be licensed under its MIT license.\n\n.. |Build| image:: https://github.com/kiwicom/schemathesis/workflows/build/badge.svg\n   :target: https://github.com/kiwicom/schemathesis/actions\n.. |Version| image:: https://img.shields.io/pypi/v/schemathesis.svg\n   :target: https://pypi.org/project/schemathesis/\n.. |Python versions| image:: https://img.shields.io/pypi/pyversions/schemathesis.svg\n   :target: https://pypi.org/project/schemathesis/\n.. |License| image:: https://img.shields.io/pypi/l/schemathesis.svg\n   :target: https://opensource.org/licenses/MIT\n\n.. _hypothesis: https://hypothesis.works/\n.. _hypothesis_jsonschema: https://github.com/Zac-HD/hypothesis-jsonschema\n.. _pytest: http://pytest.org/en/latest/\n.. _here: https://hypothesis.readthedocs.io/en/latest/reproducing.html#providing-explicit-examples\n.. _MIT license: https://opensource.org/licenses/MIT\n',
    'author': 'Dmitry Dygalo',
    'author_email': 'dmitry.dygalo@kiwi.com',
    'url': 'https://github.com/kiwicom/schemathesis',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
