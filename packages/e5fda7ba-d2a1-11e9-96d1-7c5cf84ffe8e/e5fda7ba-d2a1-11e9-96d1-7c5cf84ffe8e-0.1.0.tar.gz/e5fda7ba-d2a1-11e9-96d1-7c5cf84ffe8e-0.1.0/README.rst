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

.. |docs| image:: https://readthedocs.org/projects/lib2/badge/?style=flat
    :target: https://readthedocs.org/projects/lib2
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/python-retool/lib2.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/python-retool/lib2

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/python-retool/lib2?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/python-retool/lib2

.. |version| image:: https://img.shields.io/pypi/v/1274c9e8-d29f-11e9-96d1-7c5cf84ffe8e.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/pypi/1274c9e8-d29f-11e9-96d1-7c5cf84ffe8e

.. |commits-since| image:: https://img.shields.io/github/commits-since/python-retool/lib2/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/python-retool/lib2/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/1274c9e8-d29f-11e9-96d1-7c5cf84ffe8e.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/pypi/1274c9e8-d29f-11e9-96d1-7c5cf84ffe8e

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/1274c9e8-d29f-11e9-96d1-7c5cf84ffe8e.svg
    :alt: Supported versions
    :target: https://pypi.org/pypi/1274c9e8-d29f-11e9-96d1-7c5cf84ffe8e

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/1274c9e8-d29f-11e9-96d1-7c5cf84ffe8e.svg
    :alt: Supported implementations
    :target: https://pypi.org/pypi/1274c9e8-d29f-11e9-96d1-7c5cf84ffe8e


.. end-badges

An example package. Generated with cookiecutter-pylibrary.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install 1274c9e8-d29f-11e9-96d1-7c5cf84ffe8e

Documentation
=============


https://lib2.readthedocs.io/


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
