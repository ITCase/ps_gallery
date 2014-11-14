# -*- coding: utf-8 -*-
#
# Copyright © 2014 Petr Zelenin (po.zelenin@gmail.com)
#
# Distributed under terms of the MIT license.

import hashlib
import os
import uuid

from sqlalchemy import event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import get_history
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.sql import select
from sqlalchemy.types import CHAR, Integer, String, Text


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

    @declared_attr
    def items(cls):
        return relationship(cls.get_ref_class_name(),
                            secondary=cls.get_m2m_table())

    def __repr__(self):
        return self.name


class GalleryItemMixin(BaseMixin):

    # TODO: override 'image' field by 'sacrud.exttype.FileStore'

    description = Column(Text)
    image = Column(String, nullable=False)
    image_hash = Column(CHAR(32), unique=True, nullable=False)

    @classmethod
    def get_fk(cls):
        return '%s.%s' % (cls.__tablename__, 'image_hash')

    @declared_attr
    def galleries(cls):
        return relationship(cls.get_ref_class_name(),
                            secondary=cls.get_m2m_table())

    def __repr__(self):
        return 'Image with hash "%s"' % self.image_hash

    def generate_image_hash(self, connection):
        """Generate unique 'GalleryItemMixin.image_hash'."""
        image_hash = hashlib.md5(self.image).hexdigest()
        table = self.__class__
        check = connection.execute(
            select([table]).where(table.image_hash == image_hash))
        if check.fetchone() is not None:
            return None
        return image_hash

    def generate_unique_image(self):
        """Rename uploaded file by UUID4."""
        file_path = os.path.split(self.image)[0]
        file_name = os.path.split(self.image)[1]
        file_ext = file_name.split('.')[1]
        file_name_new = '.'.join([str(uuid.uuid4()), file_ext])
        return os.path.join(file_path, file_name_new)


@event.listens_for(GalleryItemMixin, 'before_insert', propagate=True)
@event.listens_for(GalleryItemMixin, 'before_update', propagate=True)
def event_gallery_item_change(mapper, connection, instance):
    changed = get_history(instance, 'image').has_changes()
    if changed:
        image_hash = instance.generate_image_hash(connection)
        if image_hash is None:
            connection.close()
        instance.image_hash = image_hash
        instance.image = instance.generate_unique_image()


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
