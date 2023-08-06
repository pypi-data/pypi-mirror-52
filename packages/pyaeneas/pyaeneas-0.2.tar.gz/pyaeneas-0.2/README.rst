Aeneas fullnode API client
==========================

|coverage| |PyPI version|

This package is a Python client for `Aeneas platform <http://aeneas.pm/>`__ fullnode WebSockets API.

- `API documentation <https://github.com/AeneasPlatform/Aeneas/blob/issue%23110/API.md>`__

Installation
------------

Install from PyPI by ``pip install pyaeneas``

Quickstart
----------

.. code:: python

    from pyaeneas import Aeneas

    api = Aeneas()

    # invoke signup process
    response = api.execute('Signup')
    print(response['phrase'])

    # confirm passphrase
    response = api.execute('PassPhraseSaved', {'passPhrase': response['phrase']})
    print(response)

Aeneas client uses this URI by default: ``ws://localhost:9085/aeneas``.
If you want to connect to another fullnode, pass URI as a client parameter:

.. code:: python

    from pyaeneas import Aeneas

    api = Aeneas('ws://example.com/aeneas')

Tests
-----

For running tests install and run `Aeneas fullnode <http://aeneas.pm/download/>`__,
then run a command from the parent pyaeneas directory:

``python -m unittest pyaeneas.tests.test_client``

Requirements
------------

-  Python >= 3.5.3
-  `aiohttp <https://aiohttp.readthedocs.io/en/stable/>`__

.. |coverage| image:: https://img.shields.io/codecov/c/github/AverHLV/pyaeneas.svg
.. |PyPI version| image:: https://badge.fury.io/py/pyaeneas.svg
   :target: https://badge.fury.io/py/pyaeneas
