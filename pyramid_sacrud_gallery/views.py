# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Petr Zelenin <po.zelenin@gmail.com>
#
# Distributed under terms of the MIT license.

from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config

from .common import get_model_gallery, get_model_gallery_item


@view_config(route_name='sacrud_gallery_list',
             renderer='pyramid_sacrud_gallery/gallery_list.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def gallery_list(request):
    dbsession = request.dbsession
    gallery_table = get_model_gallery(request.registry.settings)
    gallery_list = dbsession.query(gallery_table).all()
    return {
        'gallery_list': gallery_list,
    }


@view_config(route_name='sacrud_gallery_view',
             renderer='pyramid_sacrud_gallery/gallery_detail.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def gallery_view(request):
    dbsession = request.dbsession
    pk = request.matchdict['pk']
    gallery_table = get_model_gallery(request.registry.settings)
    gallery_instance = dbsession.query(gallery_table).filter(
        gallery_table.get_col_pk() == pk).one()
    return {
        'gallery': gallery_instance,
    }


@view_config(route_name='sacrud_gallery_item_view',
             renderer='pyramid_sacrud_gallery/gallery_item.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def gallery_item_view(request):
    dbsession = request.dbsession
    pk = request.matchdict['pk']
    image = request.matchdict['image']
    gallery_table = get_model_gallery(request.registry.settings)
    gallery_item_table = get_model_gallery_item(request.registry.settings)
    gallery_instance_with_item = dbsession.query(
        gallery_table, gallery_item_table
    ).filter(
        gallery_table.get_col_pk() == pk
    ).filter(
        gallery_item_table.get_col_pk() == image
    ).one()
    return {
        'gallery': gallery_instance_with_item[0],
        'image': gallery_instance_with_item[1],
    }
