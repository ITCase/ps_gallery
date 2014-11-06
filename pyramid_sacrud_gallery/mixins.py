# -*- coding: utf-8 -*-
#
# Copyright © 2014 Petr Zelenin (po.zelenin@gmail.com)
#
# Distributed under terms of the MIT license.

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import foreign, relationship, remote
from sqlalchemy.schema import ForeignKey


class GalleryMixin(object):
    name = Column(String, nullable=False)

    @classmethod
    def get_pk(cls):
        return getattr(cls, 'pyramid_sacrud_gallery_pk', 'id')

    @classmethod
    def get_db_pk(cls):
        pk = getattr(cls, cls.get_pk())
        return pk.name or cls.get_pk()

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class GalleryItemMixin(object):
    path = Column(String, nullable=False)
    description = Column(Text)

    @classmethod
    def get_pk(cls):
        return getattr(cls, 'pyramid_sacrud_gallery_item_pk', 'id')

    @classmethod
    def get_db_pk(cls):
        pk = getattr(cls, cls.get_pk())
        return pk.name or cls.get_pk()

    @classmethod
    def get_parent_class(cls):
        return getattr(cls, 'pyramid_sacrud_gallery', GalleryMixin)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def gallery_id(cls):
        gallery_cls = cls.get_parent_class()
        fk = '{0}.{1}'.format(gallery_cls.__tablename__,
                              gallery_cls.get_db_pk())
        return Column(Integer,
                      ForeignKey(fk, ondelete='CASCADE'),
                      nullable=False)

    @declared_attr
    def gallery(cls):
        gallery_cls = cls.get_parent_class()
        gallery_pk = getattr(gallery_cls, gallery_cls.get_pk(), None)
        return relationship(
            gallery_cls, foreign_keys=[cls.gallery_id],
            primaryjoin=lambda: foreign(cls.gallery_id) == remote(gallery_pk),
            backref='items'
        )
