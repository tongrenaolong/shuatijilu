from service.handler.baseHandler import BaseHandler
from service.models.problemModel import ProblemModel
from service.utils.fun import get_datetime
from service.models.userSubscriptionModel import UserSubscriptionModel
from service.models.userProblemLogModel import UserProblemLogModel
from service.models.userProblemModel import UserProblemModel

class ProblemHandler(BaseHandler):
    @classmethod
    def create_problem(cls):
        obj = cls()
        user_id = obj.user_id
        print('user_id: ',user_id)
        data = obj.post_data
        set_id = data['set_id']
        user_set_status = UserSubscriptionModel.get_one_where(
            conditions={
                "user_id": user_id,
                "set_id": set_id
            }
        )
        print('user_set_status: ',user_set_status)
        if user_set_status['authority'] == 0:
            return obj.r(msg="请联系管理员进行操作",code=200)
        problem_id_list = []
        for problem in data['problem_list']:
            res_problem = ProblemModel.get_one_where(conditions={
                'user_id': user_id,
                'set_id': set_id,
                'link': problem['link']
            })
            if res_problem:
                continue
            # 新增题目
            problem_id = ProblemModel.add_new(
                data={
                    'problem_name': problem['problem_name'],
                    'link': problem['link'],
                    'difficulty': problem['difficulty'],
                    'user_id': user_id,
                    'set_id': set_id,
                    'create_time': get_datetime()
                }
            )
            problem_id_list.append(problem_id)
        # 当前题单对应的所有用户
        user_id_list = UserSubscriptionModel.get_where(
            conditions={
                'set_id':set_id
            },
            return_fields=['user_id']
        )
        print(f'problem_id_list: {problem_id_list}, user_id_list: {user_id_list}')
        # 更新每个用户对应的题目状态
        for tem_user_id in user_id_list:
            for problem_id in problem_id_list:
                UserProblemModel.add_new(
                    data={
                        'user_id':tem_user_id['user_id'],
                        'set_id':set_id,
                        'problem_id': problem_id,
                        'status': 0,
                        'update_time': get_datetime()
                    }
                )
        return obj.r(msg='创建成功',code=200)

    @classmethod
    def get_problems(cls):
        obj = cls()
        set_id = obj.request_args['set_id']
        problem_list = ProblemModel.get_where(
            conditions={
                'set_id':set_id
            }
        )
        return obj.r(data=problem_list,code=200)

    @classmethod
    def get_problem_status(cls):
        obj = cls()
        user_id = obj.user_id
        problem_id_list = obj.post_data['problem_id_list']
        if problem_id_list is None:
            return obj.r(msg='没有需要查询到 problem_id_list',code=807)
        problem_status_list = []
        for problem_id in problem_id_list:
            problem_status = UserProblemLogModel.get_one_where(
                conditions={
                    'user_id':user_id,
                    'problem_id':problem_id
                },
                order_by={"create_time": "Desc"}
            )
            if problem_status:
                problem_status_list.append(problem_status)
        return obj.r(data=problem_status_list,code=200)

    @classmethod
    def update_status(cls):
        obj = cls()
        user_id = obj.user_id
        problem_id = obj.post_data['problem_id']
        if problem_id is None:
            return obj.r(msg='需要传递 problem_id',code=807)
        new_status = obj.post_data['new_status']
        if new_status is None:
            return obj.r(msg='需要传递 new_status',code=807)
        description = None
        image = None
        if 'description' in obj.post_data:
            description = obj.post_data['description']
        if 'image' in obj.post_data:
            image = obj.post_data['image'] # 暂时不处理
        # 判断用户是否
        problem_status = UserProblemModel.get_one_where(
            conditions={
                'user_id':user_id,
                'problem_id':problem_id
            },
        )
        if not problem_status:
            return obj.r(msg='题集中不存在对应题目',code=807)
        problem_status['status'] = new_status
        problem_status['update_time'] = get_datetime()
        if image:
            problem_status['image'] = image
        if description:
            problem_status['description'] = description
        update_result = UserProblemModel.update_by_id(
            data=problem_status,
            data_id=problem_status['id']
        )
        add_result = UserProblemLogModel.add_new(
            data={
                'user_id':user_id,
                'set_id':problem_status['set_id'],
                'problem_id': problem_id,
                'status': new_status,
                'update_time': get_datetime(),
            }
        )
        if not add_result or not update_result:
            return obj.r(msg='更新失败',code=807)
        return obj.r(msg='更新成功',code=200)
