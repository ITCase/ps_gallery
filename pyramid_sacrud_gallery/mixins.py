# -*- coding: utf-8 -*-
#
# Copyright © 2014 Petr Zelenin (po.zelenin@gmail.com)
#
# Distributed under terms of the MIT license.

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey


class BaseMixin(object):

    @classmethod
    def get_pk(cls):
        return getattr(cls, 'pyramid_sacrud_gallery_pk', 'id')

    @classmethod
    def get_db_pk(cls):
        pk = getattr(cls, cls.get_pk())
        return pk.name or cls.get_pk()

    @classmethod
    def get_col_pk(cls):
        return getattr(cls, cls.get_pk())

    @classmethod
    def get_ref_class_name(cls):
        return getattr(cls, 'pyramid_sacrud_ref_name')

    @classmethod
    def get_m2m_table(cls):
        return getattr(cls, 'pyramid_sacrud_m2m_table',
                       GalleryItemM2MMixin.__tablename__)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def get_val_pk(self):
        return getattr(self, self.get_pk())


class GalleryMixin(BaseMixin):
    name = Column(String, nullable=False)

    def __repr__(self):
        return self.name

    @declared_attr
    def items(cls):
        return relationship(cls.get_ref_class_name(),
                            secondary=cls.get_m2m_table())


class GalleryItemMixin(BaseMixin):
    name = Column(String, nullable=False)
    description = Column(Text)

    @declared_attr
    def galleries(cls):
        return relationship(cls.get_ref_class_name(),
                            secondary=cls.get_m2m_table())


class GalleryItemM2MMixin(object):

    @classmethod
    def get_gallery_class(cls):
        return getattr(cls, 'pyramid_sacrud_gallery', GalleryMixin)

    @classmethod
    def get_item_class(cls):
        return getattr(cls, 'pyramid_sacrud_gallery_item', GalleryItemMixin)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def gallery_id(cls):
        gallery_cls = cls.get_gallery_class()
        return Column(Integer,
                      ForeignKey(gallery_cls.get_col_pk(),
                                 ondelete='CASCADE'),
                      nullable=False)

    @declared_attr
    def item_id(cls):
        item_cls = cls.get_item_class()
        return Column(Integer,
                      ForeignKey(item_cls.get_col_pk(),
                                 ondelete='CASCADE'),
                      nullable=False)
