#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : WeiWang Zhang
@Time    : 2019-09-19 14:33
@File    : web_utils.py
@Desc    : 基于注解装饰器的切面工具
"""
import traceback
import logging
from django.http import HttpResponse
from django.http import HttpRequest
from wmpy_util.json_util import json_power_dump
import json
import numpy as np

logger = logging.getLogger("django_logger")


class ServiceException(Exception):
    def __init__(self, err='service error!'):
        Exception.__init__(self, err)


class IllegalDataException(Exception):
    def __init__(self, err='Illegal data error!', code=1, ):
        Exception.__init__(self, err)
        self.code = code
        self.message = err


def controller(func):
    def wrapper(*args, **kwargs):
        __name = func.__name__
        param = dict()
        try:
            request = None
            for arg in args:
                if isinstance(arg, HttpRequest):
                    request = arg
                    break
            if request is None:
                raise ServiceException("not request arg!")
            if request.method == 'POST':
                param = request.POST
            elif request.method == 'GET':
                param = request.GET
        except Exception as e:
            logger.error(traceback.format_exc())
        # 初始化返回对象
        response_data = dict(code=20001, message="", result=None)
        try:
            response_data = func(*args, **kwargs)
        except (ServiceException, IllegalDataException) as error:
            logger.error(str(error))
            response_data["message"] = str(error)
        except (ValueError, KeyError) as error:
            logger.error(" 内部错误 " + traceback.format_exc())
            response_data["message"] = "PY内部错误，请联系管理员"
        except Exception as error:
            logger.error(traceback.format_exc())
            response_data["message"] = "PY系统错误"
        if isinstance(response_data, HttpResponse):
            logger.info("%s receive_param=%s" % __name)
            return response_data
        else:
            ret_str = json_power_dump(response_data)
            logger.info(
                "%s receive_param=%s,  respond = %s" % (__name, get_cutted_param_string(param, 200), ret_str))
            callback = param.get("callback")
            if callback is not None:
                ret_str = "%s(%s)" % (callback, ret_str)
            return HttpResponse(ret_str, content_type='application/json')

    return wrapper


def get_cutted_param_string(param, len_limit=500):
    new_param = dict()
    for key in param:
        value = str(param[key])
        if len(value) > len_limit:
            value = value[:len_limit]
            value += "...(over %d)" % len_limit
        new_param[key] = value
    return str(new_param)


def kwargs_resolver(**kwargs):
    def decorator(func):
        _name = func.__name__
        _default_kwargs = kwargs

        def wrapper(*args, **kwargs):
            _default_kwargs_clone = dict(_default_kwargs)
            param = None
            try:
                request = None
                for arg in args:
                    if isinstance(arg, HttpRequest):
                        request = arg
                        break
                if request is not None:
                    if request.method == 'POST':
                        param = request.POST
                    elif request.method == 'GET':
                        param = request.GET
            except Exception as e:
                print("Resolve args failed:%s" % str(e))
            if param is not None:
                for key in _default_kwargs_clone:
                    _default_value = _default_kwargs_clone[key]
                    param_value = param.get(key)
                    if param_value is not None:
                        # 如果默认值不为None，则按照默认值的type对参数进行规范
                        if _default_value is None:
                            _default_kwargs_clone[key] = param_value
                        else:
                            _default_type = type(_default_value)
                            _default_kwargs_clone[key] = _default_type(param_value)
            kwargs.update(_default_kwargs_clone)
            ret = func(*args, **kwargs)
            return ret

        wrapper.__name__ = _name
        return wrapper

    return decorator
