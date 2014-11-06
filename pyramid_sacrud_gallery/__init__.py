# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Petr Zelenin <po.zelenin@gmail.com>
#
# Distributed under terms of the MIT license.


def includeme(config):
    config.include('pyramid_jinja2')
    config.add_jinja2_extension('jinja2.ext.with_')
    config.add_jinja2_search_path('pyramid_sacrud_gallery:templates')
    config.add_static_view('/static_sacrud_gallery',
                           'pyramid_sacrud_gallery:static')
    config.include('pyramid_sacrud_gallery.routes')
    config.scan('.views')
