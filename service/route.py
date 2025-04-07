from service.handler.userHandler import UserHandler
from service.handler.problemHandler import ProblemHandler

ROUTES = [
    {'url': '/login',
        'view_func': UserHandler.login, 'methods': ['POST']},
    {'url': '/register',
     'view_func': UserHandler.register, 'methods': ['POST']},
    {'url': '/create_problem',
     'view_func': ProblemHandler.create_problem, 'methods': ['POST']},
]