# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['jinja2_django_version']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.0,<3.0', 'django>=1.11']

setup_kwargs = {
    'name': 'jinja2-django-version',
    'version': '1.1.2',
    'description': 'A Jinja2 extension that adds django version to templates.',
    'long_description': '=====================\nJinja2 Django Version\n=====================\n\n.. image:: https://badge.fury.io/py/jinja2-python-version.svg\n    :target: https://badge.fury.io/py/jinja2-django-version\n\n.. image:: https://travis-ci.org/jmfederico/jinja2-python-version.svg?branch=master\n    :target: https://travis-ci.org/jmfederico/jinja2-django-version\n\nA Jinja extension that creates a global variable with Django version\ninformation for your Jinja2 templates:\n\nUsage\n-----\n.. code-block:: console\n\n    $ pip install jinja2-django-version\n\n.. code-block:: python\n\n    from jinja2 import Environment\n\n    env = Environment(extensions=[\'jinja2_django_version.DjangoVersionExtension\'])\n\n    # 2.0\n    template = env.from_string("{{ django_version }}")\n\n    # 2.0\n    template = env.from_string("{{ django_version.minor }}")\n\n    # 2\n    template = env.from_string("{{ django_version.major }}")\n\n    # 2.0.2\n    template = env.from_string("{{ django_version.micro }}")\n\n    template.render()\n',
    'author': 'Federico Jaramillo Martínez',
    'author_email': 'federicojaramillom@gmail.com',
    'url': 'https://github.com/jmfederico/jinja2-django-version',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
