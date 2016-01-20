[![PyPI version](https://img.shields.io/pypi/v/django-appregistration.svg)](http://badge.fury.io/py/django-appregistration) [![Build Status](https://travis-ci.org/NB-Dev/django-appregistration.svg?branch=master)](https://travis-ci.org/NB-Dev/django-appregistration) [![Coverage Status](https://coveralls.io/repos/NB-Dev/django-appregistration/badge.svg?branch=master&service=github)](https://coveralls.io/github/NB-Dev/django-appregistration?branch=master) [![Downloads](https://img.shields.io/pypi/dm/django-appregistration.svg)](https://pypi.python.org/pypi/django-appregistration/) [![Supported Python versions](https://img.shields.io/pypi/pyversions/django-appregistration.svg)](https://pypi.python.org/pypi/django-appregistration/) [![License](https://img.shields.io/pypi/l/django-appregistration.svg)](https://pypi.python.org/pypi/django-appregistration/) [![Codacy Badge](https://api.codacy.com/project/badge/grade/79d4fa62bb77478392d9535067d010c6)](https://www.codacy.com/app/tim_11/django-appregistration)

#django-appregistration


This app provides a base class to easily realize django apps that allow other apps to register parts in it.

##Requirements:

* Django >= 1.6

##Quick start

1. Install django-appregistration
    * From the pip repository: ```pip install django-appregistration```
    * or directly from github: ```pip install git+git://github.com/NB-Dev/django-apregistration.git``

#UNFINISHED

##Running the tests

The included tests can be run standalone by running the `tests/runtests.py` script. You need to have Django and
mock installed for them to run. If you also want to run coverage, you need to install it before running the tests

###v.0.0.1

- Initial implementation of `MultiTypePartRegistry` and `SingleTypePartRegistry`

## ToDos:
- Document functionality

## Maintainers
This Project is maintaned by [Northbridge Development Konrad & Schneider GbR](http://www.northbridge-development.de) Softwareentwicklung
