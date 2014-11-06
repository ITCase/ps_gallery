# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Petr Zelenin <po.zelenin@gmail.com>
#
# Distributed under terms of the MIT license.

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(name):
    with open(os.path.join(here, name)) as f:
        return f.read()

setup(
    name='pyramid_sacrud_gallery',
    version='0.0',
    url='https://github.com/ITCase/pyramid_sacrud_gallery',
    author='Petr Zelenin',
    author_email='po.zelenin@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=read('requirements.txt'),
    test_suite='pyramid_sacrud_gallery',
    description='Gallery plugin fo Pyramid SQLAlchemy CRUD.',
    long_description=read('README.rst') + '\n\n' + read('CHANGES.txt'),
    license="MIT",
    keywords='web wsgi bfg pylons pyramid',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Framework :: Pyramid ",
        "Topic :: Internet",
        "Topic :: Database",
    ],
    entry_points="""\
    [paste.app_factory]
    main = pyramid_sacrud_gallery:main
    """,
)
