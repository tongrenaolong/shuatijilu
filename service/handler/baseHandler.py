# -*- coding: utf-8 -*-
"""用户base 类"""
import os
import time
import random
from functools import wraps
from flask import session, redirect
from service.base import Base

# from setting import UPFILE_DIR
# from util.fun import get_today


class BaseHandler(Base):
    """基础操作类"""
    user_id = None
    account = None
    username = None

    def __init__(self):
        super().__init__()
        session.modified = True
        self.user_id = session.get('user_id', None)
        self.account = session.get('account', "")
        self.username = session.get('username', "")
        print(f'baseHandler session: ',session)

    # @staticmethod
    # def login_required(f):
    #     """用户登录判断"""
    #     @wraps(f)
    #     def wrapper(*args, **kwargs):
    #         if 'owner_id' in session and session.get('owner_id'):
    #             return f(*args, **kwargs)
    #
    #         obj = Base()
    #         return obj.r([], 201)
    #     return wrapper
    #
    # @classmethod
    # def _logout(cls):
    #     """用户退出登录"""
    #     if "owner_id" in session:
    #         session.pop('owner_id')
    #     if "company_name" in session:
    #         session.pop('company_name')
    #     if "active_shop_id" in session:
    #         session.pop('active_shop_id')
    #     if "shop_name" in session:
    #         session.pop('shop_name')
    #     if "company_id" in session:
    #         session.pop('company_id')
    #     obj = Base()
    #     return obj.r([], 200)
    #
    # @classmethod
    # def _set_company_name(cls, company_name):
    #     """设置公司名称"""
    #     session['company_name'] = company_name
    #
    # @classmethod
    # def _admin_logout(cls):
    #     """管理员退出登录"""
    #     if "login_m_id" in session:
    #         session.pop('login_m_id')
    #     if "login_m_name" in session:
    #         session.pop('login_m_name')
    #     if "right_code" in session:
    #         session.pop('right_code')
    #     obj = Base()
    #     return obj.r([], 200)
    #
    # @classmethod
    # def _switch_user(cls, uid, shop_name):
    #     """切换查看 店铺数据信息"""
    #     session['active_shop_id'] = uid
    #     session['shop_name'] = shop_name
    #
    # @classmethod
    # def _shop_change(cls, uid, op):
    #     """切换查看 店铺数据信息"""
    #     uid = int(uid)
    #     if op == "add":
    #         session['have_shop_ids'].append(uid)
    #     else:
    #         session['have_shop_ids'].remove(uid)
    #
    # @classmethod
    # def _upload(cls, uid, files, ext=None):
    #     """用户上传文件"""
    #     if ext is None:
    #         ext = ['.txt', '.csv', '.xlsx', '.xls', '.pdf']
    #
    #     dir_name = UPFILE_DIR + '/' + str(uid) + '/' + str(get_today())
    #     if os.path.exists(dir_name) is False:
    #         os.makedirs(dir_name)
    #     result = []
    #     msg = 'success'
    #     for file in files:
    #         file_name = file.filename
    #         _, file_extension = os.path.splitext(file_name)
    #         if file_extension.lower() not in ext:
    #             result = False
    #             msg = file_extension + " is not supported"
    #             break
    #         random_number = random.randint(10**9, 10**10 - 1)
    #         new_name = str(int(time.time())) + "_" + \
    #             str(random_number) + file_extension
    #         file_path = dir_name + '/' + new_name
    #         file.save(file_path)
    #         result_item = {
    #             'file_name': file_name.replace(file_extension, ""),
    #             'file_path': file_path.replace(UPFILE_DIR + '/' + str(uid), "")
    #         }
    #         result.append(result_item)
    #     result = result if result and len(result) > 0 else False
    #     return result, msg
    #
    # @classmethod
    # def _goto_url(cls, url):
    #     """跳转页面"""
    #     return redirect(url)
