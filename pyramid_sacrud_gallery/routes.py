# -*- coding: utf-8 -*-
#
# Copyright © 2014 Petr Zelenin (po.zelenin@gmail.com)
#
# Distributed under terms of the MIT license.


def includeme(config):
    config.add_route('sacrud_gallery_view', '/{slug}')
