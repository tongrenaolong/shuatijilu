from service.handler.userHandler import UserHandler
from service.handler.problemHandler import ProblemHandler

ROUTES = [
    {'url': '/user/login',
        'view_func': UserHandler.login, 'methods': ['POST']},
    {'url': '/user/register',
     'view_func': UserHandler.register, 'methods': ['POST']},
    {'url': '/problem/create_problem',
     'view_func': ProblemHandler.create_problem, 'methods': ['POST']},
    {'url': '/set/create_set',
     'view_func': ProblemHandler.create_problem, 'methods': ['POST']},
]