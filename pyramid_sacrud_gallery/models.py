# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Petr Zelenin <po.zelenin@gmail.com>
#
# Distributed under terms of the MIT license.

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.schema import ForeignKey

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Gallery(Base):
    __tablename__ = 'gallery'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Image(Base):
    __tablename__ = 'gallery_image'
    id = Column(Integer, primary_key=True)
    path = Column(String, nullable=False)
    description = Column(Text)
    gallery = Column(Integer, ForeignKey('gallery.id'))
