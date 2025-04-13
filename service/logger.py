# import logging
# import threading
#
# class Logger:
#     _instance = None  # 存储单例实例
#     _lock = threading.Lock()  # 用于线程安全的锁
#
#     def __new__(cls, *args, **kwargs):
#         with cls._lock:  # 确保线程安全
#             if cls._instance is None:  # 如果实例为空，创建实例
#                 cls._instance = super().__new__(cls, *args, **kwargs)
#                 cls._instance._initialize_logger()  # 初始化日志记录器
#         return cls._instance
#
#     def _initialize_logger(self):
#         """初始化日志记录器"""
#         # 创建自定义日志格式
#         log_format = '%(asctime)s [%(levelname)s] - %(module)s: %(funcName)s (line: %(lineno)d) - %(message)s'
#
#         # 设置日志记录器
#         self.logger = logging.getLogger('my_logger')
#         self.logger.setLevel(logging.DEBUG)  # 设置日志记录器的最低级别
#
#         # 创建日志处理器
#         console_handler = logging.StreamHandler()
#         console_handler.setLevel(logging.DEBUG)  # 设置控制台输出的日志级别
#
#         # 设置日志格式
#         formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
#         console_handler.setFormatter(formatter)
#
#         # 将处理器添加到日志记录器
#         self.logger.addHandler(console_handler)
#
#     def get_logger(self):
#         """返回日志记录器实例"""
#         return self.logger

from flask_login import current_user
from service.utils.fun import str_escape
from service.models.userOperationLogModel import UserOperationLogModel
from service.base import Base

class LogsServer(Base):
    obj = None
    @classmethod
    def get_obj(cls):
        """get loger object"""
        if cls.obj is None:
            cls.obj = cls()
        return cls.obj

    @classmethod
    def normal_log(cls, user_id,user_permission=0):
        """
        记录通用日志信息到数据库。

        :param method: 请求方法（如 GET、POST）。
        :param url: 请求的 URL。
        :param ip: 客户端的 IP 地址。
        :param user_agent: 客户端的 User-Agent 信息。
        :param desc: 日志描述信息。
        :param uid: 用户 ID。
        :param is_access: 是否成功访问（True 或 False）。
        :return: 返回日志记录的 ID。
        """
        obj = cls()
        info = {
            'user_id': user_id,
            'method': obj.method,
            'url': obj.url,
            'ip': obj.ip,
            'user_agent': obj.user_agent,
            'user_permission':user_permission
        }
        log_id = UserOperationLogModel.add_new(info)
        return log_id
    #
    # @classmethod
    # def login_log(cls,request, uid, is_access):
    #     """
    #     记录用户登录日志。
    #
    #     :param request: Flask 请求对象。
    #     :param uid: 用户 ID。
    #     :param is_access: 是否成功登录（True 或 False）。
    #     :return: 返回日志记录的 ID。
    #     """
    #     method = request.method
    #     url = request.path
    #     ip = request.remote_addr
    #     user_agent = str_escape(request.headers.get('User-Agent'))
    #     desc = str_escape(request.form.get('username'))
    #     return normal_log(method, url, ip, user_agent, desc, uid, is_access)
    #
    # @classmethod
    # def admin_log(cls,request, is_access, desc=None):
    #     """
    #     记录管理员操作日志。
    #
    #     :param request: Flask 请求对象。
    #     :param is_access: 是否成功操作（True 或 False）。
    #     :param desc: 日志描述信息（可选）。如果未提供，则从请求数据中提取。
    #     :return: 返回日志记录的 ID。
    #     """
    #     method = request.method
    #     url = request.path
    #     ip = request.remote_addr
    #     user_agent = str_escape(request.headers.get('User-Agent'))
    #     request_data = request.json if request.headers.get('Content-Type') == 'application/json' else request.values
    #     if desc is None:
    #         desc = str_escape(str(dict(request_data)))
    #     return normal_log(method, url, ip, user_agent, desc, current_user.id, is_access)
