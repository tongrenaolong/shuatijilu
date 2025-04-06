# -*- coding: utf-8 -*-
"""公共函数库"""
import sys
import time
from json import JSONEncoder
import simplejson

from setting import URL_DEFAULT_PREFIX
from markupsafe import escape

def get_datetime(time_type="1"):
    """时间戳转换为时间格式"""
    int_time = int(time.time())
    if "1" == time_type:
        return time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(int_time))
    return int_time

def err(info):
    """define error function, stop running  .
        定义错误处理,直接退出
    Args:
        info (string or array): error message
    """
    print(str(info))
    sys.exit()

def load_router(app, routes):
    """加载 routes

    Args:
        app (_type_): flask object
        routes (_type_):  route array
        # app.add_url_rule(rule='/test', endpoint='test', view_func=add_url_test)
        # app.add_url_rule(rule="/image", endpoint="image", view_func=image)
        # endpoint 可以理解为别名
    """
    all_endpoint = []
    prefix_url = "/" if URL_DEFAULT_PREFIX == "" else "/" + URL_DEFAULT_PREFIX + "/"

    for route in routes:
        if "url" not in route or "view_func" not in route or \
                "" == route['url'] or route['view_func'] == "":
            err("route set error" + str(route))

        url = route.pop("url").strip("/")
        if "prefix" not in route:
            url = prefix_url + url
        elif isinstance(route['prefix'], str):
            url = "/" + route['prefix'].strip("/") + "/" + url

        endpoint = route.pop("endpoint") if "endpoint" in route else ""
        if "" == endpoint:
            endpoint = url.strip("/").replace("/", "_")
        if endpoint in all_endpoint:
            err("same end_point, source url" + str(url))

        all_endpoint.append(endpoint)
        view_func = route.pop("view_func")
        # add urll
        # print(url, endpoint, route['view_func'])
        app.add_url_rule(rule=url, endpoint=endpoint,
                         view_func=view_func, **route)

def str_escape(s):
    """
    对字符串进行 XSS 过滤，返回转义后的安全字符串。

    :param s: 需要转义的字符串。
    :return: 返回转义后的字符串，如果输入为空则返回 None。
    """
    if not s:
        return None
    return str(escape(s))

def json_dumps(data, *args, **kwargs):
    """A custom JSON dumping function which passes all parameters to the
    simplejson.dumps function.
    """
    kwargs.setdefault("cls", JSONEncoder)
    kwargs.setdefault("encoding", None)
    kwargs.setdefault('ignore_nan', True)
    return simplejson.dumps(data, *args, **kwargs)
