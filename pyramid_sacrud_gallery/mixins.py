# -*- coding: utf-8 -*-
#
# Copyright © 2014 Petr Zelenin (po.zelenin@gmail.com)
#
# Distributed under terms of the MIT license.

import hashlib
import os

from sqlalchemy import event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, relationship
from sqlalchemy.orm.attributes import get_history
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.sql import select
from sqlalchemy.types import CHAR, Integer, String, Text

from pyramid_sacrud.exceptions import SacrudMessagedException
from sacrud.exttype import FileStore


UPLOAD_PATH = os.path.join('/tmp', 'pyramid_sacrud_gallery', 'upload')


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
    description = Column(Text)

    @declared_attr
    def items(cls):
        return relationship(cls.get_ref_class_name(),
                            secondary=cls.get_m2m_table())

    def __repr__(self):
        return self.name


class GalleryItemMixin(BaseMixin):

    pyramid_sacrud_upload_path = UPLOAD_PATH

    description = Column(Text)
    image_hash = Column(CHAR(32), unique=True, nullable=False)

    @classmethod
    def get_fk(cls):
        return '%s.%s' % (cls.__tablename__, 'image_hash')

    @classmethod
    def get_upload_path(cls):
        return getattr(cls, 'pyramid_sacrud_upload_path', UPLOAD_PATH)

    @declared_attr
    def image(cls):
        upload_path = cls.get_upload_path()
        return Column(FileStore(path='/static/upload/', abspath=upload_path))

    @declared_attr
    def galleries(cls):
        return relationship(cls.get_ref_class_name(),
                            secondary=cls.get_m2m_table())

    def __repr__(self):
        return 'Image with hash "%s"' % self.image_hash

    def get_image_abspath(self):
        filestore = self.__table__.columns.image.type
        return os.path.join(filestore.abspath, self.image)

    def generate_image_hash(self):
        """Generate unique 'GalleryItemMixin.image_hash'."""
        image_abspath = self.get_image_abspath()
        image_hash = hashlib.md5(image_abspath).hexdigest()
        if os.path.isfile(image_abspath):
            with open(image_abspath) as image:
                image_hash = hashlib.md5(image.read()).hexdigest()
        self.image_hash = image_hash

    def image_exists(self, connection):
        table = self.__class__
        result = connection.execute(
            select([table]).where(table.image_hash == self.image_hash)
        ).fetchone()
        return result


@event.listens_for(GalleryItemMixin, 'before_insert', propagate=True)
@event.listens_for(GalleryItemMixin, 'before_update', propagate=True)
def event_gallery_item_change(mapper, connection, instance):
    image_changed = get_history(instance, 'image').has_changes()
    if image_changed:
        instance.generate_image_hash()
    image_existed = instance.image_exists(connection)
    if image_changed and image_existed:
        raise SacrudMessagedException('This image was uploaded earlier.')


class GalleryItemM2MMixin(object):

    @classmethod
    def get_gallery_class(cls):
        return getattr(cls, 'pyramid_sacrud_gallery', GalleryMixin)

    @classmethod
    def get_item_class(cls):
        return getattr(cls, 'pyramid_sacrud_gallery_item', GalleryItemMixin)

    @staticmethod
    def __create_col_fk(ref_cls, col_type=None, fk_kwargs=None, **kwargs):
        fk_kwargs = fk_kwargs or {}
        col_type = col_type or Integer
        return Column(col_type,
                      ForeignKey(ref_cls.get_fk(), ondelete='CASCADE',
                                 **fk_kwargs),
                      nullable=False, **kwargs)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def gallery_id(cls):
        return cls.__create_col_fk(cls.get_gallery_class(), primary_key=True)

    @declared_attr
    def galleries(cls):
        return relationship(cls.get_gallery_class(),
                            backref=backref('gallery_m2m'))

    @declared_attr
    def item_id(cls):
        return cls.__create_col_fk(cls.get_item_class(), CHAR(32),
                                   primary_key=True)

    @declared_attr
    def items(cls):
        return relationship(cls.get_item_class(),
                            backref=backref('item_m2m'))
