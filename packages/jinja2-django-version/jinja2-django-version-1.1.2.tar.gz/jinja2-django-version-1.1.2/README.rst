=====================
Jinja2 Django Version
=====================

.. image:: https://badge.fury.io/py/jinja2-python-version.svg
    :target: https://badge.fury.io/py/jinja2-django-version

.. image:: https://travis-ci.org/jmfederico/jinja2-python-version.svg?branch=master
    :target: https://travis-ci.org/jmfederico/jinja2-django-version

A Jinja extension that creates a global variable with Django version
information for your Jinja2 templates:

Usage
-----
.. code-block:: console

    $ pip install jinja2-django-version

.. code-block:: python

    from jinja2 import Environment

    env = Environment(extensions=['jinja2_django_version.DjangoVersionExtension'])

    # 2.0
    template = env.from_string("{{ django_version }}")

    # 2.0
    template = env.from_string("{{ django_version.minor }}")

    # 2
    template = env.from_string("{{ django_version.major }}")

    # 2.0.2
    template = env.from_string("{{ django_version.micro }}")

    template.render()
