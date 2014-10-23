# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Petr Zelenin <po.zelenin@gmail.com>
#
# Distributed under terms of the MIT license.

import unittest
import transaction

from pyramid import testing

from sqlalchemy import create_engine

from . import TEST_DATABASE_CONNECTION_STRING
from ..models import DBSession, Base, Gallery
from ..views import gallery_view

engine = create_engine(TEST_DATABASE_CONNECTION_STRING)


class TestGalleryViewSuccessCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            galley = Gallery(name='Best gallery')
            DBSession.add(galley)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_passing_view(self):
        request = testing.DummyRequest()
        info = gallery_view(request)
        self.assertEqual(info['gallery'].name, 'Best gallery')
        self.assertEqual(info['project'], 'pyramid_sacrud_gallery')


class TestGalleryViewFailureCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        DBSession.configure(bind=engine)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_failing_view(self):

        request = testing.DummyRequest()
        info = gallery_view(request)
        print(info)
        self.assertEqual(info.status_int, 500)
