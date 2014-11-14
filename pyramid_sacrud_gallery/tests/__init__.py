# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Petr Zelenin <po.zelenin@gmail.com>
#
# Distributed under terms of the MIT license.

TEST_DATABASE_CONNECTION_STRING = 'sqlite:///:memory:'


def add_fixture(model, fixtures, session):
    instances = []
    for fixture in fixtures:
        instances.append(model(**fixture))
    session.add_all(instances)
    return instances
