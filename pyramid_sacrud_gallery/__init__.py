# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Petr Zelenin <po.zelenin@gmail.com>
#
# Distributed under terms of the MIT license.


def includeme(config):
    config.include('.assets')
    config.include('.routes')
    config.scan('.views')
