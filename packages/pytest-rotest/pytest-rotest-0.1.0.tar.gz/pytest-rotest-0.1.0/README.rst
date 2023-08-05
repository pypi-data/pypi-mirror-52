=============
pytest-rotest
=============

.. image:: https://img.shields.io/pypi/v/pytest-rotest.svg
    :target: https://pypi.org/project/pytest-rotest
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-rotest.svg
    :target: https://pypi.org/project/pytest-rotest
    :alt: Python versions

.. image:: https://travis-ci.org/UnDarkle/pytest-rotest.svg?branch=master
    :target: https://travis-ci.org/UnDarkle/pytest-rotest
    :alt: See Build Status on Travis CI

Integration with rotest

----

This `pytest` plugin was generated with `Cookiecutter` along with `@hackebrot`'s `cookiecutter-pytest-plugin` template.


Features
--------

* Full support for running Rotest tests (TestCases and TestFlows)
* Global resource manager
* Global Rotest result object
* ``--ipdbugger`` flag for setting up the ipdbugger wrapper (``-D`` or ``--debug`` in Rotest cli)
* ``--outputs`` cmd option for setting up output handlers (``-o`` or ``--outputs`` in Rotest cli)
* ``--config`` for selecting Rotest run configuration file (``-c`` or ``--config`` in Rotest cli)


Requirements
------------

* Python >= 2.7 or >= 3.6
* Rotest >= 7.3
* Pytest >= 3.5


Installation
------------

You can install "pytest-rotest" via ``pip`` from PyPI::

    $ pip install pytest-rotest


Contributing
------------
Contributions are very welcome. Tests can be run with ``tox``, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the MIT license, "pytest-rotest" is free and open source software
