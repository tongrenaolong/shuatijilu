from service.handler.baseHandler import BaseHandler
from service.utils.fun import md5,get_datetime
from service.models.userModel import UserModel
from flask import session

class UserHandler(BaseHandler):
    @classmethod
    def login(cls):
        obj = cls()
        post_data = obj.post_data
        account = post_data.get('account')
        password = md5(post_data.get('password'))
        user = UserModel.get_one_where(
            conditions={
                'account': account,
                'password': password
            })
        # Logger().get_logger().info(f'result: {user}')
        # 记录日志
        # obj.logger_obj.normal_log(
        #     method=obj.method,
        #     url=obj.base_url,
        #     ip=obj.ip,
        #     user_agent=obj.user_agent,
        #     desc="",
        #     uid=obj.user_id,
        #     is_access=1
        # )

        if user:
            session['user_id'] = user['id']
            session['account'] = user['account']
            session['username'] = user['username']
            session.modified = True
            print(f'userHandler:session: ',session)
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
                                'username': data['username'],
                                'create_time': get_datetime()
                                })
        if not res:
            return obj.r(msg="注册失败",code=807)
        return obj.r(msg="注册成功",code=200)