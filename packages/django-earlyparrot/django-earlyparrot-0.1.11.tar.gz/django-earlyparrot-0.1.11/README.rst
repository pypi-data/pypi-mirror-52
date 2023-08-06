=============================
django-earlyparrot
=============================

.. image:: https://badge.fury.io/py/django-earlyparrot.svg
    :target: https://badge.fury.io/py/django-earlyparrot

.. image:: https://requires.io/github/exolever/django-earlyparrot/requirements.svg?branch=master
     :target: https://requires.io/github/exolever/django-earlyparrot/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://travis-ci.org/exolever/django-earlyparrot.svg?branch=master
    :target: https://travis-ci.org/exolever/django-earlyparrot

.. image:: https://codecov.io/gh/exolever/django-earlyparrot/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/exolever/django-earlyparrot

.. image:: https://sonarcloud.io/api/project_badges/measure?project=exolever_django-earlyparrot&metric=alert_status
   :target: https://sonarcloud.io/dashboard?id=exolever_django-earlyparrot
  
.. image:: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat
   :target: https://github.com/exolever/django-earlyparrot/issues
    
.. image:: https://img.shields.io/badge/License-MIT-green.svg
   :target: https://opensource.org/licenses/MIT

Use EarlyParrot with Django webhooks and signals

Quickstart
----------

Install django-earlyparrot::

    pip install django-earlyparrot

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'referral',
        ...
    )

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
