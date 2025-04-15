from service.handler.baseHandler import BaseHandler
from service.models.problemModel import ProblemModel
from service.utils.fun import get_datetime
from service.models.userSubscriptionModel import UserSubscriptionModel
from service.models.userProblemLogModel import UserProblemLogModel
from service.models.userProblemModel import UserProblemModel
from service.models.problemTypeModel import ProblemTypeModel

class ProblemTypeHandler(BaseHandler):
    """题目类型相关接口"""
    @classmethod
    def create_problem_type(cls):
        """创建题目类型"""
        obj = cls()
        user_id = obj.user_id
        print(f'user_id:{user_id}')
        post_data = obj.post_data
        if not post_data:
            return obj.r(msg="没有数据",code=807)
        parent_type_id = post_data.get("parent_type_id")
        if parent_type_id is None:
            return obj.r(msg="缺少父级类型",code=807)
        type_name_list = post_data.get("type_name_list")
        if not type_name_list:
            return obj.r(msg="缺少子类类型名称",code=807)
        parent_type = ProblemTypeModel.get_one_where(
            conditions={
                'type_id':parent_type_id,
            }
        )
        if not parent_type:
            return obj.r(msg="父级类型不存在",code=807)
        error_list = []
        for type_name in type_name_list:
            result = ProblemTypeModel.get_one_where(
                conditions={
                    'type_name':type_name
                }
            )
            if result:
                error_list.append(type_name)
                continue
            ProblemTypeModel.add_new(data={
                "type_name":type_name,
                'type_level':parent_type['type_level']+1,
                "parent_type_id":parent_type_id,
            })
        if error_list:
            return obj.r(msg="以下类型已存在",code=807,data={"error_list":error_list})
        return obj.r(msg="创建成功",code=200)

    @classmethod
    def delete_problem_type(cls):
        """删除题目类型"""
        obj = cls()
        user_id = obj.user_id
        post_data = obj.post_data
        if not post_data:
            return obj.r(msg="没有数据",code=807)

        type_id_list = post_data.get("type_id_list")
        if not type_id_list:
            return obj.r(msg="缺少类型ID列表",code=807)
            
        not_found_list = []

        def delete_type_and_children(type_id):
            # 递归删除子类型
            children = ProblemTypeModel.get_where(
                conditions={
                    'parent_type_id': type_id
                }
            )
            for child in children:
                delete_type_and_children(child['type_id'])
            
            # 删除当前类型
            ProblemTypeModel.delete(
                conditions={
                    'type_id': type_id
                }
            )

        for type_id in type_id_list:
            # 查找要删除的类型
            type_to_delete = ProblemTypeModel.get_one_where(
                conditions={
                    'type_id': type_id
                }
            )
            if not type_to_delete:
                not_found_list.append(type_id)
                continue
                
            # 递归删除该类型及其所有子类型
            delete_type_and_children(type_id)
            
        if not_found_list:
            return obj.r(msg="以下类型ID不存在",code=807,data={
                "not_found_list": not_found_list,
            })
        return obj.r(msg="删除成功",code=200)

    @classmethod
    def update_problem_type(cls):
        """更新题目类型"""
        obj = cls()
        user_id = obj.user_id
        post_data = obj.post_data
        if not post_data:
            return obj.r(msg="没有数据",code=807)
            
        type_id_list = post_data.get("type_id_list")
        if not type_id_list:
            return obj.r(msg="缺少更新数据",code=807)
            
        success_list = []
        
        for type_id, update_data in type_id_list.items():
            # 检查要更新的类型是否存在
            type_to_update = ProblemTypeModel.get_one_where(
                conditions={
                    'type_id': type_id
                }
            )
            if not type_to_update:
                continue
                
            # 如果要更新父级ID，检查新父级是否存在
            new_parent_id = update_data.get('parent_type_id')
            if new_parent_id is not None:
                parent_type = ProblemTypeModel.get_one_where(
                    conditions={
                        'type_id': new_parent_id
                    }
                )
                if not parent_type:
                    continue
                    
                # 检查是否形成循环引用
                if str(type_id) == str(new_parent_id):
                    continue
                    
                # 更新type_level
                update_data['type_level'] = parent_type['type_level'] + 1
            
            # 如果要更新类型名，检查新名称是否已存在
            new_type_name = update_data.get('type_name')
            if new_type_name:
                existing_type = ProblemTypeModel.get_one_where(
                    conditions={
                        'type_name': new_type_name,
                        'type_id': ['!=', type_id]
                    }
                )
                if existing_type:
                    continue
            
            # 执行更新
            ProblemTypeModel.update_where(
                conditions={'type_id': type_id},
                data=update_data
            )
        return obj.r(msg="更新完成", code=200, data={
            "success_list": success_list,
            "error_list": error_list
        })