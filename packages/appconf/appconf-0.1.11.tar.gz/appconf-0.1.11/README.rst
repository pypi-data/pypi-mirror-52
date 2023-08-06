###########
appconf
###########

.. readme_inclusion_marker


Running tests
-------------

.. code-block:: bash

    $ pytest -c ops/tools/pytest.ini tests/unit


Running linters
---------------

.. code-block:: bash

    $ pep8 -c ops/tools/pep8.ini src/appconf test/appconf
    $ pylint -c ops/tools/pylint.ini src/appconf test/appconf


Building docs
-------------

.. code-block:: bash

    $ sphinx-build -b html -d .build/docs docs docs/html
