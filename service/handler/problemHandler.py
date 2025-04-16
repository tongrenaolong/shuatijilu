from service.handler.baseHandler import BaseHandler
from service.models.problemModel import ProblemModel
from service.utils.fun import get_datetime
from service.models.userSubscriptionModel import UserSubscriptionModel
from service.models.userProblemLogModel import UserProblemLogModel
from service.models.userProblemModel import UserProblemModel
from service.models.problemTypeModel import ProblemTypeModel

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

    @classmethod
    def update_problem(cls):
        """批量更新题目信息"""
        obj = cls()
        user_id = obj.user_id
        data = obj.post_data
        
        try:
            set_id = int(data.get('set_id'))
            problem_list = data.get('problem_list', [])
        except (ValueError, TypeError):
            return obj.r(msg="参数类型错误", code=807)
            
        if not problem_list:
            return obj.r(msg="题目列表不能为空", code=807)
            
        # 验证用户权限
        user_set_status = UserSubscriptionModel.get_one_where(
            conditions={
                "user_id": user_id,
                "set_id": set_id
            }
        )
        if not user_set_status or user_set_status['authority'] == 0:
            return obj.r(msg="没有修改权限", code=807)
            
        success_list = []
        error_list = []
        
        for problem in problem_list:
            # 验证必填字段
            if 'problem_id' not in problem:
                error_list.append({
                    'problem_name': problem.get('problem_name', '未知'),
                    'reason': '缺少必填字段 problem_id'
                })
                continue
                
            # 获取当前题目信息
            current_problem = ProblemModel.get_one_where(
                conditions={
                    'id': problem['problem_id'],
                    'set_id': set_id
                }
            )
            if not current_problem:
                error_list.append({
                    'problem_id': problem['problem_id'],
                    'reason': '题目不存在或不属于该题单'
                })
                continue
                
            # 构建更新数据
            update_data = {}
            
            # 处理选填字段
            if 'problem_name' in problem:
                update_data['problem_name'] = problem['problem_name']
            if 'link' in problem:
                update_data['link'] = problem['link']
            if 'difficulty' in problem:
                try:
                    update_data['difficulty'] = int(problem['difficulty'])
                except (ValueError, TypeError):
                    error_list.append({
                        'problem_id': problem['problem_id'],
                        'reason': '难度值必须为整数'
                    })
                    continue
            if 'type_id' in problem:
                try:
                    type_id = int(problem['type_id'])
                    # 验证题目类型是否存在
                    type_exists = ProblemTypeModel.get_one_where(
                        conditions={
                            'id': type_id
                        }
                    )
                    if not type_exists:
                        error_list.append({
                            'problem_id': problem['problem_id'],
                            'reason': f'题目类型 {type_id} 不存在'
                        })
                        continue
                    update_data['type_id'] = type_id
                except (ValueError, TypeError):
                    error_list.append({
                        'problem_id': problem['problem_id'],
                        'reason': '类型ID必须为整数'
                    })
                    continue
            
            # 如果没有需要更新的字段，跳过
            if not update_data:
                continue
                
            # 更新题目
            result = ProblemModel.update_by_id(
                data=update_data,
                data_id=problem['problem_id']
            )
            
            if result:
                success_list.append(problem['problem_id'])
            else:
                error_list.append({
                    'problem_id': problem['problem_id'],
                    'reason': '更新失败'
                })
                
        return obj.r(
            msg='处理完成',
            code=200,
            data={
                'success_count': len(success_list),
                'success_list': success_list,
                'error_list': error_list if error_list else None
            }
        )
