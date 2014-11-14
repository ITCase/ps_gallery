# -*- coding: utf-8 -*-
#
# Copyright © 2014 Petr Zelenin (po.zelenin@gmail.com)
#
# Distributed under terms of the MIT license.

import unittest

from pyramid_sacrud_gallery.common import (
    get_model_by_name, get_model_gallery, get_model_gallery_item
)

from . import Gallery, GalleryItem, GalleryItemM2M


class TestCommon(unittest.TestCase):

    def setUp(self):
        models = ['Gallery', 'GalleryItem', 'GalleryItemM2M']
        self.settings = {}
        for model in models:
            key = 'pyramid_sacrud_gallery.model_locations.%s' % model
            value = 'pyramid_sacrud_gallery.tests:%s' % model
            self.settings[key] = value

    def tearDown(self):
        pass

    def test_imports_by_settings(self):
        self.assertEqual(get_model_gallery(self.settings), Gallery)
        self.assertEqual(get_model_gallery_item(self.settings), GalleryItem)
        self.assertEqual(get_model_by_name(self.settings, 'GalleryItemM2M'),
                         GalleryItemM2M)
