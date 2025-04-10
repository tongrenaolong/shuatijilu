from service.handler.baseHandler import BaseHandler
from service.utils.fun import md5,get_datetime
from service.models.userModel import UserModel
from service.models.problemSetModel import ProblemSetModel
from service.models.userSubscriptionModel import UserSubscriptionModel
from flask import session

class ProblemSetHandler(BaseHandler):
    @classmethod
    def create_set(cls):
        obj = cls()
        user_id = obj.id
        post_data = obj.post_data
        if not post_data:
            return obj.r(msg="没有数据",code=807)
        post_data.update({"create_time":get_datetime()})
        set_id = ProblemSetModel.add_new(data=post_data)
        UserSubscriptionModel.add_new(data={
            "user_id": user_id,
            "set_id": set_id,
            "authority": 1
        })
        if not set_id:
            return obj.r(msg="创建失败",code=807)
        return obj.r(msg="创建成功",code=200,data={"set_id":set_id})
