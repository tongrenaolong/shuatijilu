# -*- coding: utf-8 -*-

class Server():
    app_obj = None

    @classmethod
    def get_app(cls):
        if cls.app_obj:
            return cls.app_obj
        else:
            from flask import Flask
            from setting import DEBUG,MYSQL_URL,ROOT
            from service.logger import LogsServer
            app = Flask(__name__, template_folder=ROOT + '/util/templates')
            app.debug = DEBUG
            app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_URL
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            app.config['logger_obj'] = LogsServer.get_obj()
            cls.app_obj = app
            return cls.app_obj
