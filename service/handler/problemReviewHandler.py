from service.handler.baseHandler import BaseHandler
from service.models.problemModel import ProblemModel
from service.utils.fun import get_datetime
from service.models.userSubscriptionModel import UserSubscriptionModel
from service.models.userProblemLogModel import UserProblemLogModel
from service.models.userProblemModel import UserProblemModel
from service.models.problemTypeModel import ProblemTypeModel

class ProblemReviewHandler(BaseHandler):
    """题目复习计划"""
    @classmethod
    def create_review_plan(cls):
        """创建题目复习计划——后台任务"""
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
        error_list = []  # 记录验证失败的题目
        
        for problem in data['problem_list']:
            # 验证题目类型是否存在
            type_exists = ProblemTypeModel.get_one_where(
                conditions={
                    'type_id': problem['type_id']
                }
            )
            if not type_exists:
                error_list.append({
                    'problem_name': problem['problem_name'],
                    'reason': f'题目类型 {problem["type_id"]} 不存在'
                })
                continue
                
            # 验证题目是否已存在
            res_problem = ProblemModel.get_one_where(
                conditions={
                    'user_id': user_id,
                    'set_id': set_id,
                    'link': problem['link']
                }
            )
            if res_problem:
                error_list.append({
                    'problem_name': problem['problem_name'],
                    'reason': '题目链接已存在'
                })
                continue
                
            # 新增题目
            problem_id = ProblemModel.add_new(
                data={
                    'problem_name': problem['problem_name'],
                    'link': problem['link'],
                    'difficulty': problem['difficulty'],
                    'type_id': problem['type_id'],  # 添加题目类型ID
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
                
        return obj.r(msg='创建成功', 
                    code=200, 
                    data={
                        'success_count': len(problem_id_list),
                        'error_list': error_list if error_list else None
                    })