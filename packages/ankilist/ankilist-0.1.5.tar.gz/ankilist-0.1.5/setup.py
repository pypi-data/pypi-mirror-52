# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['ankilist']
entry_points = \
{'console_scripts': ['ankilist = ankilist:main']}

setup_kwargs = {
    'name': 'ankilist',
    'version': '0.1.5',
    'description': 'Lite google translate console client and anki list generator',
    'long_description': None,
    'author': 'VladislavNekto',
    'author_email': 'vladislav.nekto.dev@gmail.com',
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '==3.7.4',
}


setup(**setup_kwargs)
