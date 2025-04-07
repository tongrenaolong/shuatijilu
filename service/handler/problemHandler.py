from service.handler.baseHandler import BaseHandler
from service.models.problemModel import ProblemModel

class ProblemHandler(BaseHandler):
    @classmethod
    def create_problem(cls):
        obj = cls()
        user_id = obj.id
        data = obj.post_data
        set_id = data['set_id']
        problem_list = []
        for problem in data['problem_list']:
            res_problem = ProblemModel.get_one_where(conditions={
                'user_id': user_id,
                'set_id':set_id,
                'link':problem['link']
            })
            if res_problem:
                continue
            problem_list.append({
                'problem_name': problem['problem_name'],
                'link': problem['link'],
                'difficulty': problem['difficulty'],
                'user_id':user_id,
                'set_id':set_id
            })
        res_status,msg = ProblemModel.add_multy(problem_list)
        if not res_status:
            return obj.r(msg=msg,code=807)
        return obj.r(msg=msg,code=200)