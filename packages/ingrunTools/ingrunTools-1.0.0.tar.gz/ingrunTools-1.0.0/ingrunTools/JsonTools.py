import json

from django.db import models
from django.http import HttpResponse


def get_json_success(msg=None):
    if msg is None:
        msg = '成功'
    dick = {'code': 1, 'msg': msg, 'data': ''}
    return HttpResponse(json.dumps(dick, ensure_ascii=False))


def get_json_error(msg=None):
    if msg is None:
        msg = '错误'
    dick = {'code': 0, 'msg': msg, 'data': ''}
    return HttpResponse(json.dumps(dick, ensure_ascii=False))


def get_json_models(ser, data, code=None, msg=None):
    """
    将一条模型数据完整返回
    :param ser:   这是模型序列化器
    :param data:  模型数据  可一个 models 或者是一个 queryset
    :param code:
    :param msg:
    :return:
    """

    code = get_code(data, code)
    msg = get_msg(code, msg)
    ser2 = ser(data, many=(not isinstance(data, models.Model)))
    dick = {'code': code, 'msg': msg, 'data': ser2.data}
    return HttpResponse(json.dumps(dick, ensure_ascii=False))


def get_code(data, code=None):
    if code:
        return code
    else:
        if data:
            code = 1
        else:
            code = 0
        return code


def get_msg(code=None, msg=None):
    if msg:
        return msg
    else:
        if code:
            msg = "操作成功！"
        else:
            msg = "操作失败！"
        return msg
