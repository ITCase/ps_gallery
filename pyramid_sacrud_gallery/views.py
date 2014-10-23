# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Petr Zelenin <po.zelenin@gmail.com>
#
# Distributed under terms of the MIT license.

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import DBSession, Gallery


@view_config(route_name='home', renderer='templates/gallery.pt')
def gallery_view(request):
    try:
        gallery = DBSession.query(Gallery).filter(
            Gallery.name == 'Best gallery').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain',
                        status_int=500)
    return {'gallery': gallery, 'project': 'pyramid_sacrud_gallery'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pyramid_sacrud_gallery_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
