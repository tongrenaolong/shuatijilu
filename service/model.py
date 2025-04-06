# -*- coding: utf-8 -*-

class Main():
    db = None

    @classmethod
    def get_obj(cls):
        if cls.db:
            return cls.db
        else:
            from service.utils import Server
            from models.initModel import DbBase
            cls.db = DbBase(Server.get_app())
            return cls.db

db = Main.get_obj()
