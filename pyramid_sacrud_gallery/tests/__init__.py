# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Petr Zelenin <po.zelenin@gmail.com>
#
# Distributed under terms of the MIT license.

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer


from pyramid_sacrud_gallery.mixins import (
    GalleryMixin, GalleryItemMixin, GalleryItemM2MMixin
)

Base = declarative_base()

TEST_DATABASE_CONNECTION_STRING = 'sqlite:///:memory:'


def add_fixture(model, fixtures, session):
    instances = []
    for fixture in fixtures:
        instances.append(model(**fixture))
    session.add_all(instances)


class Gallery(Base, GalleryMixin):

    pk = Column('id', Integer, primary_key=True)
    pyramid_sacrud_gallery_pk = 'pk'
    pyramid_sacrud_ref_name = 'GalleryItem'
    pyramid_sacrud_m2m_table = 'galleryitemm2m'


class GalleryItem(Base, GalleryItemMixin):

    pk = Column('id', Integer, primary_key=True)
    pyramid_sacrud_gallery_pk = 'pk'

    pyramid_sacrud_ref_name = 'Gallery'
    pyramid_sacrud_m2m_table = 'galleryitemm2m'


class GalleryItemM2M(GalleryItemM2MMixin, Base):

    id = Column(Integer, primary_key=True)

    pyramid_sacrud_gallery = Gallery
    pyramid_sacrud_gallery_item = GalleryItem
