[![PyPI version](https://img.shields.io/pypi/v/django-appregistration.svg)](http://badge.fury.io/py/django-appregistration) [![Build Status](https://travis-ci.org/NB-Dev/django-appregistration.svg?branch=master)](https://travis-ci.org/NB-Dev/django-appregistration) [![Coverage Status](https://coveralls.io/repos/NB-Dev/django-appregistration/badge.svg?branch=master&service=github)](https://coveralls.io/github/NB-Dev/django-appregistration?branch=master) [![Downloads](https://img.shields.io/pypi/dm/django-appregistration.svg)](https://pypi.python.org/pypi/django-appregistration/) [![Supported Python versions](https://img.shields.io/pypi/pyversions/django-appregistration.svg)](https://pypi.python.org/pypi/django-appregistration/) [![License](https://img.shields.io/pypi/l/django-appregistration.svg)](https://pypi.python.org/pypi/django-appregistration/) [![Codacy Badge](https://api.codacy.com/project/badge/grade/e9e55c2658d54801b6b29a1f52173dcf)](https://www.codacy.com/app/tim_11/django-appregistation)

#django-appregistration


This app provides a base class to easily realize django apps that allow other apps to register parts in it.

##Requirements:

* Django >= 1.6

##Installation

    * From the pip repository: ```pip install django-appregistration```
    * or directly from github: ```pip install git+git://github.com/NB-Dev/django-apregistration.git``

##Usage

django-appregistration provides two base classes for the registration of modules from other apps:
`MultiListPartRegistry` and `SingleListPartRegistry`. While both have the same basic functionality, in the
`MultiListPartRegistry` multiple distinct lists of objects can be collected, while the `SingleListPartRegistry` only
contains a single list.

To implement a `...PartRegistry` in your app, create a subclass of the `...PartRegistry` or your choice in a convenient
place in your application. There are some attributes you can overwrite in your Subclass:

* `part_class` (required): The (parent) class of the objects that are allowed to be inserted into your Registry

* `call_function_subpath` (required): The subpath to the function that is to be called by the registry on load (details,
see below)

* `ignore_django_namespace`(default: True): If true, any app that starts with `django.` in your `INSTALLED_APPS` will be
ignored on load time.

To prevent arbitrary items to be inserted into your Registry the `...PartRegistry` classes check each added element to
be an instance of the class that is set as the `part_class` attribute of the your Registry.
 
When the Registry tries to load elements from the `INSTALLED_APPS`, it iterates over the apps and tries, for each to get
the sub module / function that is defined in the `call_function_subpath`. It then checks if the retrieved object is
callable and calls it if so passing the Registry itself as only call parameter.

To register elements with the Registry you therefore need to implement the appropriate function at
`call_function_subpath` in an app that is listed in the `INSTALLED_APPS`. The implemented function then needs to call
the `add_item` function on the passed registry.

### MultiListPartRegistry
The following functions are available:

#### add_part(list, part)
Adds the part given by the `part` parameter to the list with the name given by the `list` parameter.

### get(list)
Returns the parts in the list with the name given by the `list` parameter. The elements are sorted before they are
returned.

### sort_parts(parts)
Can be overwritten to define a custom ordering of the parts. The default function simply returns the list unordered.

### load()
When called, the class is initialized and loads the available parts into its list cache. Does nothing if the `load()`
was already called. Is called automatically by the `get()` function. There is no need to call it explicitly unless you
want to initialize the class before the first list is retrieved.

### reset()
Resets the Registry to its initial state so that the parts will be reloaded the next time the `load()` function is
called. Usually there is no need to call this as it only adds extra overhead when the parts need to be loaded again.

##Running the tests

The included tests can be run standalone by running the `tests/runtests.py` script. You need to have Django and
mock installed for them to run. If you also want to run coverage, you need to install it before running the tests

###Development
- Rename `Type` to `List` in class names

###v.0.0.1

- Initial implementation of `MultiTypePartRegistry` and `SingleTypePartRegistry`


## Maintainers
This Project is maintaned by [Northbridge Development Konrad & Schneider GbR](http://www.northbridge-development.de) Softwareentwicklung
