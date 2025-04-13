from service.handler.baseHandler import BaseHandler
from service.models.userProblemLogModel import UserProblemLogModel
from service.utils.fun import md5,get_datetime
from service.models.problemModel import ProblemModel
from service.models.userProblemSetLogModel import UserProblemSetLogModel
from service.models.problemSetModel import ProblemSetModel
from service.models.userSubscriptionModel import UserSubscriptionModel

class ProblemSetHandler(BaseHandler):
    @classmethod
    def create_set(cls):
        obj = cls()
        user_id = obj.user_id
        print(f'user_id:{user_id}')
        post_data = obj.post_data
        if not post_data:
            return obj.r(msg="没有数据",code=807)
        post_data.update({"create_time":get_datetime()})
        set_id = ProblemSetModel.add_new(data=post_data)
        UserProblemSetLogModel.add_new(data={
            "user_id": user_id,
            "set_id": set_id,
            'op_type': 1,
            'update_time': get_datetime()
        })
        print(f'set_id:{set_id}')
        UserSubscriptionModel.add_new(data={
            "user_id": user_id,
            "set_id": set_id,
            "authority": 1
        })
        if not set_id:
            return obj.r(msg="创建失败",code=807)
        return obj.r(msg="创建成功",code=200,data={"set_id":set_id})

    @classmethod
    def get_problem_sets(cls):
        obj = cls()
        user_id = obj.user_id
        user_subscription_ret = UserSubscriptionModel.get_where(
            conditions={
                "user_id": user_id
            },
        )
        set_id_list = [sub['set_id'] for sub in user_subscription_ret]
        set_problem_list = ProblemSetModel.get_where(
            conditions={
                'id':  ['in', set_id_list]
            }
        )
        return obj.r(data=set_problem_list,code=200)

    @classmethod
    def _get_authority(cls, user_id,set_id):
        user_set_status = UserSubscriptionModel.get_where(
            conditions={
                'user_id': user_id,
                'set_id': set_id
            }
        )
        if not user_set_status:
            return False
        return user_set_status['authority']

    @classmethod
    def delete_problem_set(cls):
        obj = cls()
        user_id = obj.user_id
        set_id_list = obj.request_args['set_id_list']
        if set_id_list is None:
            return obj.r(msg="没有需要删除的题集",code=807)
        for set_id in set_id_list:
            authority = cls._get_authority(user_id,set_id)
            user_id_list = []
            # 暂时将用户对应的表关系进行删除
            user_id_list.append(user_id)
            if authority:
                tem_user_id_list = UserSubscriptionModel.get_where(
                    conditions={
                        'set_id': set_id,
                        'authority': 0
                    }
                )
                user_id_list += tem_user_id_list
            UserSubscriptionModel.delete(
                conditions={
                    'user_id': ['in', user_id_list],
                    'set_id': set_id
                }
            )
            # UserProblemSetLogModel 添加操作日志
            data = []
            for tem_user_id in user_id_list:
                tem_data = {
                    'user_id': tem_user_id,
                    'set_id': set_id,
                    'op_type': 3,
                    'update_time': get_datetime(),
                }
                if tem_user_id == user_id:
                    tem_data['op_type'] = 0
                data.append(tem_data)
            UserSubscriptionModel.add_multy(
                data=data
            )
        return obj.r(msg='删除成功',code=200)

    @classmethod
    def search_problem_set_name(cls):
        obj = cls()
        set_name = obj.request_args['set_name']
        if set_name is None:
            return obj.r(msg="需要传递 set_name",code=807)
        problem_set_list = ProblemSetModel.get_where(
            conditions={
                'set_name': ['like', set_name]
            }
        )
        if not problem_set_list:
            return obj.r(msg='查找失败',code=807)
        return obj.r(data=problem_set_list,code=200)

    @classmethod
    def join_problem_set(cls):
        obj = cls()
        user_id = obj.user_id
        set_id_list = obj.post_data['set_id_list']
        if set_id_list is None:
            return obj.r(msg="需要传递 set_id_list",code=807)
        for set_id in set_id_list:
            user_subscription_ret = UserSubscriptionModel.get_one_where(
                conditions={
                    'user_id': user_id,
                    'set_id': set_id
                }
            )
            if user_subscription_ret:
                continue
            # 加入题集
            UserSubscriptionModel.add_new(
                data={
                    'user_id': user_id,
                    'set_id': set_id,
                    'authority': 0
                }
            )
            # 记录题集操作日志
            UserProblemSetLogModel.add_new(
                data={
                    'user_id': user_id,
                    'set_id': set_id,
                    'op_type': 2,
                    'update_time': get_datetime(),
                }
            )
            # 建立 题目和用户状态
            problem_id_list = ProblemModel.get_where(
                conditions={
                    'set_id': set_id
                }
            )
            for problem_id in problem_id_list:
                UserProblemLogModel.add_new(
                    data={
                        'user_id':user_id,
                        'problem_id': problem_id,
                        'status': 0,
                        'update_time': get_datetime()
                    }
                )
        return obj.r(msg="加入成功",code=200)