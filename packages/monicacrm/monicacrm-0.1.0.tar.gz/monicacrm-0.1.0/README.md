Overview
========

[![PyPI Latest Release][img_pypi_rels]][pypi_link]
[![Supported Python Versions][img_pypi_supp]][pypi_link]
[![Supported Python Implementations][img_pypi_impl]][pypi_link]

[pypi_link]: https://pypi.org/project/monicacrm
[img_pypi_rels]: https://img.shields.io/pypi/v/monicacrm.svg "PyPI Latest Release"
[img_pypi_supp]: https://img.shields.io/pypi/pyversions/monicacrm.svg "Supported Python Versions"
[img_pypi_impl]: https://img.shields.io/pypi/implementation/monicacrm.svg "Supported Python Implementations"

This is python-monicacrm vv0.1.0., a client library for the [Free/Libre MonicaHQ.com personal relationships manager](https://monicahq.com) to assist with tasks like bulk import.

The initial goal was to enable entry of contacts using CSV, including adding tags and tasks at time-of-entry. Additional goals may arise. I'm happy to receive suggestions and code contributions also.

This repo was initialised with an overzealous and badly-opinionated cookiecutter, so some inconsistencies may appear at the margins. If you find mention of proprietary SASS crap in here somewhere, it's possible that it's cookiecutter cruft that I missed.

Installation
============

pip install monicacrm


Documentation
=============

This is a personal project so I'm not committing great effort here, but I will try to docstring the project where possible, and use informative argument names. I'll probably come back here and offer some sample code, also. For the most part this acts as a convenience layer over the Monica API, so [if you're familiar with that][monica_api_docs] you'll figure this out, too.

[monica_api_docs]: https://www.monicahq.com/api/overview

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

    PYTEST_ADDOPTS=--cov-append tox
