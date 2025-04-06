# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool
from setting import SQLALCHEMY_ENABLE_POOL_PRE_PING, SQLALCHEMY_DISABLE_POOL
from service.utils.fun import json_dumps


class DbBase(SQLAlchemy):

    def apply_driver_hacks(self, app, info, options):
        options.update(json_serializer=json_dumps)
        if SQLALCHEMY_ENABLE_POOL_PRE_PING:
            options.update(pool_pre_ping=True)
        super(DbBase, self).apply_driver_hacks(app, info, options)

    def apply_pool_defaults(self, app, options):
        super(DbBase, self).apply_pool_defaults(app, options)
        if SQLALCHEMY_ENABLE_POOL_PRE_PING:
            options["pool_pre_ping"] = True
        if SQLALCHEMY_DISABLE_POOL:
            options["poolclass"] = NullPool
            # Remove options NullPool does not support:
            options.pop("max_overflow", None)
    pass
