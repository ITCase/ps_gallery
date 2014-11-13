# -*- coding: utf-8 -*-
#
# Copyright © 2014 Petr Zelenin (po.zelenin@gmail.com)
#
# Distributed under terms of the MIT license.

import os

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import CHAR, Integer, String, Text

from sacrud.exttype import FileStore

file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')


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
    def get_fk(cls):
        return cls.get_col_pk()

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
    description = Column(Text)
    image = Column(FileStore(path='/static/uploaded/',
                             abspath=os.path.join(file_path, 'uploaded')))
    image_hash = Column(CHAR(32))

    @classmethod
    def get_fk(cls):
        return '%s.%s' % (cls.__tablename__, 'image_hash')

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

    @staticmethod
    def __create_col_fk(ref_cls, fk_kwargs=None, **kwargs):
        fk_kwargs = fk_kwargs or {}
        return Column(Integer,
                      ForeignKey(ref_cls.get_fk(), ondelete='CASCADE',
                                 **fk_kwargs),
                      nullable=False, **kwargs)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def gallery_id(cls):
        return cls.__create_col_fk(cls.get_gallery_class())

    @declared_attr
    def item_id(cls):
        return cls.__create_col_fk(cls.get_item_class())
