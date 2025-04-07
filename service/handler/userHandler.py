from service.handler.baseHandler import BaseHandler
from service.utils.fun import md5
from service.models.userModel import UserModel

class UserHandler(BaseHandler):
    @classmethod
    def login(cls):
        obj = cls()
        post_data = cls.post_data
        user_info = post_data.get('user_info')
        password = md5(user_info['password'])
        user = UserModel.get_one_where(conditions={'account': user_info['account'], 'password': password})
        # Logger().get_logger().info(f'result: {user}')
        # 记录日志
        obj.logger_obj.normal_log(
            method=obj.method,
            url=obj.base_url,
            ip=obj.ip,
            user_agent=obj.user_agent,
            desc="",
            uid=obj.id,
            is_access=1
        )

        if user:
            print("Login successful!")
            # session.permanent = True
            # user_id = user.user_id
            # Logger().get_logger().info(user.user_id)
            # user_info['user_id'] = user_id
            # session['user_info'] = user_info
            # Logger().get_logger().info("session[user_info]: ", session['user_info'])
            return obj.r(msg="login success",code=200)
        else:
            print("Invalid username or password.")
            return obj.r(msg="登录失败",code=200)

    @classmethod
    def register(cls):
        obj = cls()
        data = obj.post_data
        password = md5(data['password'])
        res = UserModel.add_new(data={'account': data['account'],
                                'password': password,
                                'username': data['username']
                                })
        if not res:
            return obj.r(msg="注册失败",code=807)
        return obj.r(msg="注册成功",code=200)