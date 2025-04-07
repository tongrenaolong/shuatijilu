# -*- coding: utf-8 -*-
"""基础类"""
import json
from decimal import Decimal
from flask import make_response, request, current_app
from service.utils.fun import get_datetime,str_escape

class Base:
    """基础类"""
    user_lang = 'ZH'
    # message = None
    logger_obj = None
    method = None
    ip = None
    user_agent = None
    request_args = None
    post_data = None

    def __init__(self):
        # set default Language
        # self.message = current_app.config['MESSAGE']
        request_type = request.content_type
        if request_type and 'application/json' in request_type:
            # json
            data = request.json if request.json and request.method == 'POST' else {}
            data_files = None
        elif request_type and "form" in request.content_type:
            # form
            data = request.form if request.method == 'POST' else {}
            data_files = request.files if request.method == 'POST' else None
        else:
            data = data_files = None

        self.post_data = data
        self.method = request.method
        self.request_args = request.args if request.args else {}
        # self.request_files = data_files
        self.logger_obj = current_app.config['logger_obj']
        self.ip = request.remote_addr
        port = request.host.split(':')[1] if ':' in request.host else ''
        self.user_agent = str_escape(request.headers.get('User-Agent'))
        self.base_url = "https" + '://' + \
            request.host.split(':')[0] + (':' + port if port else '')

    def r(self, data=None, code=200, message_type='sys', return_type='json', msg=None):
        """front return

        Args:
            data (list, optional): _description_. Defaults to [].
            code (int, optional): _description_. Defaults to 200.
            message_type (str, optional): _description_. Defaults to 'sys'.
            return_type (str, optional): _description_. Defaults to 'json'.

        Returns:
            _type_: json
        """
        if not data:
            data = []
        message_type = str(message_type.lower())
        if msg is None:
            msg = self.message[message_type][self.user_lang][str(code)] \
                if message_type in self.message and \
                self.user_lang in self.message[message_type] and \
                str(code) in self.message[message_type][self.user_lang] \
                else "Unkonwn " + str(message_type) + " " + self.user_lang
        if 'json' == return_type:
            data = self.convert_decimals(data)
            json_data = json.dumps({
                "code": code,
                "data": data,
                "msg": msg
            }, sort_keys=False, ensure_ascii=False)

            # 创建响应，并设置Content-Type
            response = make_response(json_data)
            response.headers['Content-Type'] = 'application/json'
            return response

        response = make_response(data)
        response.headers['Content-Type'] = 'text/plain'
        return response

    @classmethod
    def convert_decimals(cls, obj):
        """
        递归地将所有 Decimal 类型转换为 float
        """
        if isinstance(obj, Decimal):
            return float(obj)  # 或者返回 str(obj) 根据需要
        if isinstance(obj, list):
            return [cls.convert_decimals(item) for item in obj]
        if isinstance(obj, dict):
            return {key: cls.convert_decimals(value) for key, value in obj.items()}

        return obj  # 如果不是 Decimal 类型，直接返回