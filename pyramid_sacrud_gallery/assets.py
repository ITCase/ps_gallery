#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Assets for pyramid_sacrud_gallery
"""


def includeme(config):
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('pyramid_sacrud_gallery:templates')
    config.add_static_view('static_sacrud_gallery',
                           'pyramid_sacrud_gallery:static')
