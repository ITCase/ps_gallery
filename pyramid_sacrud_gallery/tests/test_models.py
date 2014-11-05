# -*- coding: utf-8 -*-
#
# Copyright © 2014 Petr Zelenin (po.zelenin@gmail.com)
#
# Distributed under terms of the MIT license.

import unittest

import transaction

from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

# in-project
from pyramid_sacrud_gallery.mixins import GalleryMixin, GalleryItemMixin

# in-module
from pyramid_sacrud_gallery.tests import TEST_DATABASE_CONNECTION_STRING

Base = declarative_base()
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


class Gallery(Base, GalleryMixin):

    pk = Column('id', Integer, primary_key=True)
    pyramid_sacrud_gallery_pk = 'pk'


class GalleryItem(Base, GalleryItemMixin):

    pk = Column('id', Integer, primary_key=True)
    pyramid_sacrud_gallery_item_pk = 'pk'

    pyramid_sacrud_gallery = Gallery


def add_fixtures(model, fixtures, session):
    for fixture in fixtures:
        session.add(model(**fixture))


def add_galleries(session):
    galleries = [
        {'pk': 1, 'name': 'Best gallery'}
    ]
    items = []
    for x in xrange(1, 10):
        items.append({'pk': x, 'path': 'image/%s.jpg' % x, 'gallery_id': 1})
    add_fixtures(Gallery, galleries, session)
    add_fixtures(GalleryItem, items, session)


class TestGallery(unittest.TestCase):

    def setUp(self):
        engine = create_engine(TEST_DATABASE_CONNECTION_STRING)
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            add_galleries(DBSession)

    def tearDown(self):
        DBSession.remove()

    def test_mixins_attrs(self):
        """Check mixins attrs auto apply to classes."""
        self.assertEqual(Gallery.get_pk(), 'pk')
        self.assertEqual(Gallery.get_db_pk(), 'id')
        self.assertEqual(Gallery.__tablename__, 'gallery')

        self.assertEqual(GalleryItem.get_pk(), 'pk')
        self.assertEqual(GalleryItem.get_db_pk(), 'id')
        self.assertEqual(GalleryItem.__tablename__, 'galleryitem')

    def test_mixins_fks(self):
        """Check GalleryItemMixin has ForeignKey to GalleryMixin."""
        self.assertTrue(hasattr(GalleryItem, 'gallery_id'))
        self.assertTrue(hasattr(GalleryItem, 'gallery'))
        self.assertTrue(hasattr(Gallery, 'items'))
