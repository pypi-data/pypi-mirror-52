========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/01d61084-d29e-11e9-96d1-7c5cf84ffe8e/badge/?style=flat
    :target: https://readthedocs.org/projects/01d61084-d29e-11e9-96d1-7c5cf84ffe8e
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/python-retool/01d61084-d29e-11e9-96d1-7c5cf84ffe8e.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/python-retool/01d61084-d29e-11e9-96d1-7c5cf84ffe8e

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/python-retool/01d61084-d29e-11e9-96d1-7c5cf84ffe8e?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/python-retool/01d61084-d29e-11e9-96d1-7c5cf84ffe8e

.. |version| image:: https://img.shields.io/pypi/v/01d61084-d29e-11e9-96d1-7c5cf84ffe8e.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/pypi/01d61084-d29e-11e9-96d1-7c5cf84ffe8e

.. |commits-since| image:: https://img.shields.io/github/commits-since/python-retool/01d61084-d29e-11e9-96d1-7c5cf84ffe8e/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/python-retool/01d61084-d29e-11e9-96d1-7c5cf84ffe8e/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/01d61084-d29e-11e9-96d1-7c5cf84ffe8e.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/pypi/01d61084-d29e-11e9-96d1-7c5cf84ffe8e

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/01d61084-d29e-11e9-96d1-7c5cf84ffe8e.svg
    :alt: Supported versions
    :target: https://pypi.org/pypi/01d61084-d29e-11e9-96d1-7c5cf84ffe8e

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/01d61084-d29e-11e9-96d1-7c5cf84ffe8e.svg
    :alt: Supported implementations
    :target: https://pypi.org/pypi/01d61084-d29e-11e9-96d1-7c5cf84ffe8e


.. end-badges

An example package. Generated with cookiecutter-pylibrary.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install 01d61084-d29e-11e9-96d1-7c5cf84ffe8e

Documentation
=============


https://01d61084-d29e-11e9-96d1-7c5cf84ffe8e.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
