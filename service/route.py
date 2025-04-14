from service.handler.problemSetHandler import ProblemSetHandler
from service.handler.userHandler import UserHandler
from service.handler.problemHandler import ProblemHandler
from service.back_work.taskHandler import TestTask
from service.rpc.ai_rpc import AiRPCService
from service.rpc.email_rpc import EmailRPC

ROUTES = [
    # 用户
    {'url': '/user/login',
        'view_func': UserHandler.login, 'methods': ['POST']},
    {'url': '/user/register',
     'view_func': UserHandler.register, 'methods': ['POST']},

    # 题目
    {'url': '/problem/create_problem',
     'view_func': ProblemHandler.create_problem, 'methods': ['POST']},
    {'url': '/problem/get_problems',
     'view_func': ProblemHandler.get_problems, 'methods': ['GET']},
    {'url': '/problem/update_status',
     'view_func': ProblemHandler.update_status, 'methods': ['POST']},
    {'url': '/problem/get_problem_status',
     'view_func': ProblemHandler.get_problem_status, 'methods': ['POST']},

    # 题单
    {'url': '/set/create_problem_set',
     'view_func': ProblemSetHandler.create_set, 'methods': ['POST']},
    {'url': '/set/get_problem_sets',
     'view_func': ProblemSetHandler.get_problem_sets, 'methods': ['GET']},
    {'url': '/set/delete_problem_set',
     'view_func': ProblemSetHandler.delete_problem_set, 'methods': ['POST']},
    {'url': '/set/search_problem_set_name',
     'view_func': ProblemSetHandler.search_problem_set_name, 'methods': ['POST']},
    {'url': '/set/join_problem_set',
     'view_func': ProblemSetHandler.join_problem_set, 'methods': ['POST']},
]