.. :changelog:

History
-------

0.1.0 (2017-12-29)
++++++++++++++++++

* First release on PyPI.
* Initial models and REST API

0.2.0 (2018-01-05)
++++++++++++++++++

`0.2.0 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.1.0...v0.2.0>`_

* Improved REST API filters

0.2.1 (2018-01-09)
++++++++++++++++++

`0.2.1 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.2.0...v0.2.1>`_

* Updated packages and fixed issue with migrations

0.2.2 (2018-01-12)
++++++++++++++++++

`0.2.2 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.2.1...v0.2.2>`_

* Fixed route names for SimpleRouter

0.3.0 (2018-02-09)
++++++++++++++++++

`0.3.0 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.2.2...v0.3.0>`_

0.3.1 (2018-03-14)
++++++++++++++++++

`0.3.1 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.3.0...v0.3.1>`_

* Updated requirements
* Updated choices for file type choices to be more comprehensive

0.4.0 (2018-03-23)
++++++++++++++++++

`0.4.0 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.3.1...v0.4.0>`_

* Added property for File model for easy access to display type


0.5.0 (2018-03-30)
++++++++++++++++++

`0.5.0 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.4.0...v0.5.0>`_

* Added additional file type choices

0.6.0 (2018-04-03)
++++++++++++++++++

`0.6.0 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.5.0...v0.6.0>`_

* Added support for GraphQL

0.7.0 (2018-04-07)
++++++++++++++++++

`0.7.0 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.6.0...v0.7.0>`_

* Added support for GraphQL

0.7.1 (2018-04-18)
++++++++++++++++++

`0.7.1 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.7.0...v0.7.1>`_

* #27 - Fixed file type issues
* Updated 3rd party libs

0.7.2 (2018-05-16)
++++++++++++++++++

`0.7.2 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.7.1...v0.7.2>`_

* Updated 3rd party libs
* Updated setup.py to read from requirements.txt

0.8.0 (2018-06-01)
++++++++++++++++++

`0.8.0 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.7.2...v0.8.0>`_

* Removed support for GraphQL - useless here.  Applications using GraphQL can set up schema with models

0.8.1 (2018-08-13)
++++++++++++++++++

`0.8.1 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.8.0...v0.8.1>`_

* Updated 3rd party requirements. Some requirements had changed so it was causing failures

0.8.2 (2018-10-29)
++++++++++++++++++

`0.8.2 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.8.1...v0.8.2>`_

* Updated 3rd party requirements.

0.8.3 (2019-01-08)
++++++++++++++++++

`0.8.3 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.8.2...v0.8.3>`_

* Updated 3rd party requirements.

0.8.4 (2019-02-08)
++++++++++++++++++

`0.8.4 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.8.3...v0.8.4>`_

* Updated 3rd party requirements.
* Refactored tests

0.8.5 (2019-04-10)
++++++++++++++++++

`0.8.5 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.8.4...v0.8.5>`_

* Updated 3rd party requirements.
* Updated travis to use xenial distribution. Django 2.1 dropped support for SQLite < 3.8.3

0.8.6 (2019-05-31)
++++++++++++++++++

`0.8.6 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.8.5...v0.8.6>`_

* Updated package to use latest cookiecutter template

0.8.7 (2019-07-26)
++++++++++++++++++

`0.8.7 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.8.6...v0.8.7>`_

* Updated 3rd party requirements.

0.8.8 (2019-08-09)
++++++++++++++++++

`0.8.8 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.8.7...v0.8.8>`_

* Updated 3rd party requirements.
* Added support for excel file types

0.9.0 (2019-09-09)
++++++++++++++++++

`0.9.0 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.8.8...v0.9.0>`_

* Updated 3rd party requirements.
* Added FileField and hash (to detect duplicates)

0.9.1 (2019-09-09)
++++++++++++++++++

`0.9.1 Changelog <https://github.com/chopdgd/django-data-sources-tracking/compare/v0.9.0...v0.9.1>`_

* Hotfix to fix broken migration.  It could not access create_hash method on File class
