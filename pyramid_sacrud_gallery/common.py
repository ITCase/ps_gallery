# -*- coding: utf-8 -*-
#
# Copyright © 2014 Petr Zelenin (po.zelenin@gmail.com)
#
# Distributed under terms of the MIT license.

from pyramid_sacrud.common import import_from_string


def get_model_by_name(settings, name):
    model = settings['pyramid_sacrud_gallery.model_locations.%s' % name]
    return import_from_string(model)


def get_model_gallery(settings):
    return get_model_by_name(settings, 'Gallery')


def get_model_gallery_item(settings):
    return get_model_by_name(settings, 'GalleryItem')
